#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('zhihu.db')
tagconn = sqlite3.connect('tagUrlSet.db')
cursor = conn.execute('''select question,url,vote_up
                from zhihu;''')

for item in cursor:
    print 'question : ',item[0]
    print 'url : ',item[1]
    print 'vote_up : ',item[2]       


cursor = tagconn.execute('''select name,url,checked from tagUrlSet 
                            where checked = 1;''')
cursor = tagconn.execute('''select name,url,checked from tagUrlSet 
                            where url = 'https://www.zhihu.com/topic/19552162';''')

for item in cursor:
    print 'name:',item[0]
    print 'url:',item[1]
    print 'checked:',item[2]

count = conn.execute('''select count(*) from zhihu;''')
for i in count:
    print i[0]

count = tagconn.execute('''select count(*) from tagUrlSet;''')
for i in count:
    print i[0]

conn.close
tagconn.close
