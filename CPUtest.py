import time
import threading

#for CPU test
class test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not exiting:
            pass

exiting = False
for i in range(0,5):
    thread = test()
    thread.deamon = True
    thread.start()
try:
    while True:
        time.sleep(2)
    pass
except :
    exiting = True
    exit()
