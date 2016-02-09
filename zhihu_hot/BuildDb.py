#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os

conn = sqlite3.connect('zhihu.db')
conn.execute('''drop table zhihu''')


conn.execute('''create table zhihu
                    (question varchar(100) not null,
                    url varchar(100) not null,
                    vote_up varchar(10) not null);''')
conn.commit()
conn.close()

conn= sqlite3.connect('tagUrlSet.db')
conn.execute('''drop table tagUrlSet''')
conn.execute('''create table tagUrlSet
                    (name varchar(100) not null,
                    url varchar(100) not null,
                    checked int not null);''')
conn.commit()
conn.close()


#os.remove('CurrentSearch.data')
#os.remove('zhihu.log')
