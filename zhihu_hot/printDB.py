#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

def printQuestion():
    cursor = conn.execute('''select question,url,vote_up
                    from zhihu;''')
    
    for item in cursor:
        print 'question : ',item[0]
        print 'url : ',item[1]
        print 'vote_up : ',item[2]       

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
count = conn.execute('''select count(*) from zhihu;''')
for i in count:
    print i[0]
count = tagconn.execute('''select count(*) from tagUrlSet
                            where checked = 0;''')
for i in count:
    print i[0]
conn.close
tagconn.close
