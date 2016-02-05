#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sqlite3
import urllib
import urllib2
import Queue
from bs4 import BeautifulSoup

#for main thread
class TagSearcher:
    def __init__(self,channel):
        self.channel = channel
        self.queue = self.channel.queue

    def start(self):
        self.getID()
        logging.info('Successfully Got ID.')
        #bulid topicIDSet
        for topicID in self.ID:
            self.searchTag(topicID)

    def getID(self):
        #exit when open fail
        response = self.channel.getOpen('https://www.zhihu.com/topics')
        if response is None:
            logging.warning('Error When Getting ID.')
            exit()
        IDsoup = BeautifulSoup(response.read())
        #if error abort
        self.ID = IDsoup.find(
                'ul',class_='zm-topic-cat-main clearfix').find_all('li')
    
    def searchTag(self,ID):
        topicsUrl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
        hasmore = True
        offset = 0
        while hasmore:
            params = ('''{
                    "topic_id":%s,
                    "offset":%d,
                    "hash_id":"93c19ac70419d81ede4a80676ae4842b"}'''%(ID['data-id'],offset)
                    )
            offset += 20
            data = urllib.urlencode(
                {"method":'next',
                'params':params,
                '_xsrf':'2cec849bfdc0744a4936d508a2a6d16b'})
            #get tags
            result = self.channel.postOpen(topicsUrl,data)
            if result is None:#open fail
                break
            result = result.read().decode("unicode-escape").replace('\\','')
            soup = BeautifulSoup(result)
            tags = soup.find_all('div',class_='item')
            if len(tags) != 20:
                hasmore = False
            #do datamine(for each tag)
            for tag in tags:
                self.queue.put(tag) 
                logging.debug('Putting tag %s in queue.'%(tag.strong.string))

