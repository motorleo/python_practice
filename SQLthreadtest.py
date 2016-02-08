import threading
import sqlite3
import time

class Write(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        conn = sqlite3.connect('test.db')
        try:
            for i in range(0,500):
                print "thread-write:",i
                conn.execute('''insert into test values(1);''')
        except:
            raise
        time.sleep(10)
        conn.commit()
        conn.close()



class Read(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(1)
        conn = sqlite3.connect('test.db')
        try:
            for i in range(0,500):
                print 'thread-read:',i
                #conn.execute('''select test from test;''')
                conn.execute('''insert into test values(1);''')
        except:
            raise
        time.sleep(2)
        conn.close()
        


def buildDB():
    conn = sqlite3.connect('test.db')
    conn.execute('''create table test1(test int);''')
    conn.close()


def main():
    write = Write()
    write.start()
    read = Read()
    read.start()
    write.join()
    read.join()

main()
