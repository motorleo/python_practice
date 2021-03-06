#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sqlite3
import threading
import Queue
from bs4 import BeautifulSoup
from TagSearcher import TagItem

class DatamineThread(threading.Thread):
    def __init__(self,channel):
        threading.Thread.__init__(self)
        self.channel = channel
        self.queue = channel.queue
        self.answerUrlSet = channel.answerUrlSet
        self.tagUrlSet = channel.tagUrlSet

    def run(self):
        self.zhihuConn = sqlite3.connect('zhihu.db')
        self.tagConn = sqlite3.connect('tagUrlSet.db')
        while not self.channel.exiting:
            tag = self.queue.get()
            self.datamine(tag)
            self.queue.task_done()
        logging.info('Exiting.')
        self.zhihuConn.close()
        self.tagConn.close()

    def datamine(self,tag):
        logging.info('Dealing with tag:%s'%(tag.tagName))
        self.channel.tagSetLock.acquire()
        logging.debug('tagSetLock.')
        if tag.tagUrl in self.tagUrlSet:
            self.channel.tagSetLock.release()
            logging.debug('tagSetUnlock.')
            logging.info('Repeat Tag!')
            return
        self.channel.tagSetLock.release()
        logging.debug('tagSetUnlock.')
        nextPage = True
        pagenum = 1
        pageUrl = tag.tagUrl + '/top-answers'
        repeatTag = False
        firstPage = True
        #for each page
        while nextPage:
            page = self.channel.getOpen(pageUrl)
            if page is None:
                break
            soup = BeautifulSoup(page)
            #check rename tag
            if firstPage:
                firstPage = False
                tagUrl = soup.find('link',rel='canonical')['href']
                if tagUrl != tag.tagUrl:
                    logging.info('Rename Tag!')
                    break
            #build next pageurl
            pagenum += 1
            pageUrl = tag.tagUrl + '/top-answers?page=%d'%(pagenum)
            #for each question
            items = soup.find_all('div',class_='feed-main')
            if len(items) == 0:
                nextPage = False
            for item in items:
                if self.channel.exiting:
                    return
                #question
                question = item.h2.a.string
                #href
                href = item.find('div',class_='zm-item-rich-text')
                if href is None:
                    continue
                if href.attrs.has_key('data-entry-url'):
                    href = href['data-entry-url'].replace('\\','')
                else:
                    continue
                self.channel.answerSetLock.acquire()
                logging.debug('answerSetLock.')
                if href in self.answerUrlSet:
                    logging.info('%s Drop For Repeat'%(question))
                    self.channel.answerSetLock.release()
                    logging.debug('answerSetUNLock.')
                    continue
                else:
                    self.answerUrlSet.add(href)
                self.channel.answerSetLock.release()
                logging.debug('answerSetUNLock.')
                #vote_up
                vote_up = item.find('span',class_='count')
                if vote_up is None:
                    continue
                vote_up = int(vote_up.string.replace('K','000'))
                if vote_up < 1000:
                    logging.info('%s  %d , Drop'%(question,vote_up))
                    nextPage = False
                    break
                #save
                self.channel.answerSaveLock.acquire()
                logging.debug('answerSaveLock.')
                self.zhihuConn.execute('''insert into zhihu
                                values(?,?,?);''',(question,href,vote_up))
                self.zhihuConn.commit()
                self.channel.answerSaveLock.release()
                logging.debug('answerSaveUNLock.')
                logging.info('%s  URL:%s  vote_up:%d,Successfully saved.'%(question,href,vote_up))
        #tag finish
        self.channel.tagSetLock.acquire()
        logging.debug('tagSetLock.')
        self.tagUrlSet.add(tag.tagUrl)
        self.channel.tagSetLock.release()
        url = tag.tagUrl.replace("'","''")
        self.channel.tagSaveLock.acquire()
        logging.debug('tagSetUnLock.')
        self.tagConn.execute('''update tagUrlSet set checked = 1
                                where url = '%s';'''%(url))
        self.tagConn.commit()
        self.channel.tagSaveLock.release()
        logging.info('Tag:%s is done.'%(tag.tagName))
 
