#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sqlite3
import threading
import Queue
from bs4 import BeautifulSoup

class DatamineThread(threading.Thread):
    def __init__(self,channel):
        threading.Thread.__init__(self)
        self.channel = channel
        self.queue = channel.queue

    def run(self):
        self.conn = sqlite3.connect('zhihu.db')
        logging.info('Thread Start Running.')
        while not self.channel.exiting:
            tag = self.queue.get()
            self.datamine(tag)
            self.queue.task_done()
        logging.info('Exiting.')
        self.jobsDone()

    def jobsDone(self):
        self.conn.close()

    def datamine(self,tag):
        nextPage = True
        pageHref = 'https://www.zhihu.com' + tag.a['href'].replace('\\','')
        pagenum = 1
        pageUrl = pageHref + '/top-answers'
        logging.info('Dealing with tag:%s'%(tag.strong.string))
        repeatTag = False
        firstPage = True
        #for each page
        while nextPage:
            if self.channel.exiting:
                return
            page = self.channel.getOpen(pageUrl)
            if page is None:
                break
            soup = BeautifulSoup(page.read())
            #check rename tag
            if firstPage:
                firstPage = False
                tagURL = soup.find('link',rel='canonical')['href']
                cursor = self.conn.execute('''select url from tagUrlSet
                                              where url = '%s';'''%(tagURL))
                if cursor.fetchone() is not None:
                    logging.info('Repeat Tag!')
                    repeatTag = True
                    break
            #build next pageurl
            pagenum += 1
            pageUrl = pageHref + '/top-answers?page=%d'%(pagenum)
            #for each question
            for item in soup.find_all('div',class_='feed-main'):
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
                cursor = self.conn.execute('''select url from zhihu
                                              where url = '%s';'''%(href))
                if cursor.fetchone() is not None:
                    logging.info('%s Drop For Repeat'%(question))
                    continue
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
                logging.info('%s  URL:%s  vote_up:%d , ready to save.'%(question,href,vote_up))
                self.conn.execute('''insert into zhihu
                                values(?,?,?);''',(question,href,vote_up))
                self.conn.commit()
                logging.info('%s , Successfully saved!'%(question))
        #tag finish
        if not repeatTag:
            self.conn.execute('''insert into tagUrlSet values('%s');'''%(pageHref))
            self.conn.commit()
            logging.info('Tag:%s is done.'%(tag.strong.string))
 
