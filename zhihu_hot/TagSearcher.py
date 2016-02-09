#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import logging
import sqlite3
import urllib
import Queue
import cPickle
from bs4 import BeautifulSoup

#for main thread
class TagSearcher:
    def __init__(self,channel):
        self.channel = channel
        self.queue = channel.queue
        self.tagUrlSet = channel.tagUrlSet


    def start(self):
        self.getID()
        logging.info('Successfully Got ID.')
        self.conn = sqlite3.connect('tagUrlSet.db')
        self.putLastTag()
        self.continueWork()
        self.conn.close()

    def firstTimeWork(self):
        for topicID in self.ID:
            ID = topicID['data-id']
            self.searchTag(ID)


    def continueWork(self):
        if not os.path.isfile('CurrentSearch.data'):#first time to work
            self.firstTimeWork()
        else:
            f = file('CurrentSearch.data')
            try:
                lastID = cPickle.load(f)
                lastOffset = cPickle.load(f)
            except EOFError:
                f.close()
                self.firstTimeWork()
                return
            f.close()
            index = 0#last ID index
            if not (lastID == 0 and lastOffset == 0):
                self.searchTag(lastID,lastOffset)
                while self.ID[index]['data-id'] != lastID:
                    index += 1
                index += 1
            #begin with last ID
            for i in range(index,len(self.ID)):
                ID = self.ID[i]['data-id']
                self.searchTag(ID)
 

    def saveCurrentSearch(self,ID,offset):
        f = file('CurrentSearch.data','w')
        cPickle.dump(ID,f)
        cPickle.dump(offset,f)
        f.close()
        logging.info('CurrentSearch--ID:{},offset:{}'.format(ID,offset))

    def putLastTag(self):
        cursor = self.conn.execute('''select name,url from tagUrlSet
                                      where checked = 0;''')
        for tag in cursor:
            self.queue.put(TagItem(tag[0],tag[1]))
            #logging.debug('Put tag %s in queue.'%(tag[0]))

    def getID(self):
        #exit when open fail
        response = self.channel.getOpen('https://www.zhihu.com/topics')
        if response is None:
            logging.warning('Error When Getting ID.')
            exit()
        IDsoup = BeautifulSoup(response)
        #if error then abort
        self.ID = IDsoup.find(
                'ul',class_='zm-topic-cat-main clearfix').find_all('li')
    
    def searchTag(self,ID,offset=0):
        topicsUrl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
        hasmore = True
        while hasmore:
            self.saveCurrentSearch(ID,offset)
            params = ('''{
                    "topic_id":%s,
                    "offset":%d,
                    "hash_id":"93c19ac70419d81ede4a80676ae4842b"}'''%(ID,offset)
                    )
            data = urllib.urlencode(
                {"method":'next',
                'params':params,
                '_xsrf':'2cec849bfdc0744a4936d508a2a6d16b'})
            offset += 20
            #get tags
            result = self.channel.postOpen(topicsUrl,data)
            if result is None:#open fail
                break
            result = result.decode("unicode-escape").replace('\\','')
            soup = BeautifulSoup(result)
            tags = soup.find_all('div',class_='item')
            if len(tags) != 20:
                hasmore = False
            #do datamine(for each tag)
            self.channel.tagSaveLock.acquire()
            for tag in tags:
                tagName = tag.strong.string
                tagUrl = 'https://www.zhihu.com' + tag.a['href'].replace('\\','')
                cursor = self.conn.execute('''select url from tagUrlSet
                                               where url = '%s';'''%(tagUrl))
                if cursor.fetchone() is not None:
                    continue
                self.queue.put(TagItem(tagName,tagUrl)) 
                self.conn.execute('''insert into tagUrlSet
                                   values(?,?,0);''',(tagName,tagUrl))
                #logging.debug('Put tag %s in queue.'%(tagName))
            #done
            self.conn.commit()
            self.channel.tagSaveLock.release()
            time.sleep(0.5)#avoid lock

class TagItem:
    def __init__(self,tagName,tagUrl):
        self.tagName = tagName
        self.tagUrl =tagUrl
