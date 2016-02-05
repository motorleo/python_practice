#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('zhihu.db')
cursor = conn.execute('''select question,url,vote_up
                from zhihu;''')

for item in cursor:
    print 'question : ',item[0]
    print 'url : ',item[1]
    print 'vote_up : ',item[2]       


cursor = conn.execute('''select url from tagUrlSet;''')

for item in cursor:
    print 'url : ',item[0]

count = conn.execute('''select count(*) from zhihu;''')
for i in count:
    print i[0]

count = conn.execute('''select count(*) from tagUrlSet;''')
for i in count:
    print i[0]

conn.close
