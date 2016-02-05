#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from sets import Set

conn = sqlite3.connect('zhihu.db')
#cursor = conn.cursor()
#cursor.execute('''drop table zhihu''')
#cursor.execute('''create table zhihu
#                    (question varchar(100) not null,
#                    url varchar(100) not null,
#                    vote_up varchar(10) not null);''')

cursor = conn.execute('''select url
                       from zhihu;''')
for item in cursor:
    print item[0]

i = '/question/28808973/answer/42163583'
test = conn.execute('''select url from zhihu
                        where url = '{}';'''.format(i))
print test.fetchall()

count = conn.execute('''select count(*) from zhihu;''')
print count.fetchone()[0]
#conn.execute('''delete from zhihu;''')
conn.commit()
conn.close()
