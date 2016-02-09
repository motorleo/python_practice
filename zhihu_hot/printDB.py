#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

def printQuestion():
    cursor = conn.execute('''select question,url,vote_up
                    from zhihu where vote_up >= 10000;''')
    #cursor = conn.execute('''select question,url,vote_up
    #                from zhihu where url = '/question/24078583/answer/26668990';''')
    
    for item in cursor:
        print 'question : ',item[0]
        print 'url : ',item[1]
        print 'vote_up : ',item[2],type(item[2])

def printUnchecked():
    cursor = tagconn.execute('''select name,url,checked from tagUrlSet 
                                where checked = 0;''')
    
    for item in cursor:
        print 'name:',item[0]
        print 'url:',item[1]
        print 'checked:',item[2]

conn = sqlite3.connect('zhihu.db')
tagconn = sqlite3.connect('tagUrlSet.db')
printUnchecked()
printQuestion()
count = conn.execute('''select count(*) from zhihu;''')
print 'question:',count.fetchone()[0]
count = tagconn.execute('''select count(*) from tagUrlSet
                            where checked = 0;''')
print 'unchecked:',count.fetchone()[0]
count = tagconn.execute('''select count(*) from tagUrlSet
                            where checked = 1;''')
print 'checked:',count.fetchone()[0]
conn.close
tagconn.close
