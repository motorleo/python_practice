#!/usr/bin/python
# -*- coding: utf-8 -*-

import Queue
import logging
import sys
from DatamineThread import DatamineThread
from TagSearcher import TagSearcher
from ZhihuChannel import ZhihuChannel

class ZhihuHotSpider:
    def __init__(self,threadNum):
        logFormat = '%(asctime)s--%(threadName)s : %(message)s'
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
            queue.join()
        except KeyboardInterrupt:
            channel.exiting = True
            logging.info('Sending Exit Message!')
        print 'Exiting Main Thread.'


def main():
    if len(sys.argv) < 3:
        print 'Please Enter The Email And The Password.'
        exit()
    spider = ZhihuHotSpider(2)

if __name__ == '__main__':
    main()
