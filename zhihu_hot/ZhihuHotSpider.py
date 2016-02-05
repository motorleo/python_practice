#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Queue
import logging
import sys
from DatamineThread import DatamineThread
from TagSearcher import TagSearcher
from ZhihuChannel import ZhihuChannel

class ZhihuHotSpider:
    def __init__(self,threadNum):
        logFormat = '%(asctime)s--%(levelname)s--%(threadName)s : %(message)s'
        #logging.basicConfig(filename='zhihu.log',level=logging.INFO,format=logFormat)
        logging.basicConfig(level=logging.INFO,format=logFormat)
        queue = Queue.Queue()
        channel = ZhihuChannel(queue,sys.argv[1],sys.argv[2])
        #build threads
        for i in range(0,threadNum):
            thread = DatamineThread(channel)
            thread.deamon = True
            thread.start()
        try:
            #put tag in queue
            tagSearcher = TagSearcher(channel)
            tagSearcher.start()
            #wait for queue's empty
            while not queue.empty():
                time.sleep(1)
        except KeyboardInterrupt:
            channel.exiting = True
            logging.info('Sending Exit Message!')
        logging.info('Exiting Main Thread.')


def main():
    if len(sys.argv) < 3:
        print 'Please Enter The Email And The Password.'
        exit()
    spider = ZhihuHotSpider(3)#3 thread

if __name__ == '__main__':
    main()
