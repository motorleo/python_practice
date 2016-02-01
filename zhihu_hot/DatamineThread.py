#!/usr/bin/python
# -*- coding: utf-8 -*-

from sets import Set
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
        self.urlset = channel.urlset

    def run(self):
        self.conn = sqlite3.connect('zhihu.db')
        while not self.channel.exiting:
            tag = self.queue.get()
            self.datamine(tag)
            self.queue.task_done()
        logging.info('Exiting')
        self.jobsDone()

    def jobsDone(self):
        self.conn.close()

    def datamine(self,tag):
        nextPage = True
        pageHref = tag.a['href'].replace('\\','')
        pagenum = 1
        pageUrl = 'https://www.zhihu.com' + pageHref + '/top-answers'
        #for each page
        while nextPage:
            page = self.channel.getOpen(pageUrl)
            if page is None:
                break
            soup = BeautifulSoup(page.read())
            #build next pageurl
            pagenum += 1
            pageUrl = ('https://www.zhihu.com' +
                      pageHref + '/top-answers?page=%d'%(pagenum))
            #for each question
            for item in soup.find_all('div',class_='feed-main'):
                question = item.h2.a.string
                logging.info(question)
                vote_up = item.find('span',class_='count').string
                if 'K' not in vote_up:
                    logging.info(u'{},丢弃'.format(vote_up))
                    nextPage = False
                    break
                else:
                    logging.info('{}'.format(vote_up))
                href = item.find('div',class_='zm-item-rich-text')
                href = href['data-entry-url'].replace('\\','')
                logging.info('{}'.format(href))
                if href in self.urlset:
                    logging.info(u'重复丢弃')
                    continue
                else:
                    self.urlset.add(href)
                self.conn.execute('''insert into zhihu
                                values('%s','%s','%s');'''%(question,href,vote_up))
                self.conn.commit()
                logging.info('Successfully saved!')
 
