import os
import threading
import time
import cPickle
import logging

tset = set()
class add(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for i in range(0,10):
            tset.add(i) 
            print 'add',i
            time.sleep(1)

class read(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(1)
        for i in range(0,10):
            print tset
            time.sleep(1)

thread1 = add()
thread2 = read()
thread1.start()
thread2.start()
thread2.join()
thread1.join()
