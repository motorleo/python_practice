#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('zhihu.db')
cursor = conn.cursor()
cursor.execute('''create table zhihu
                    (question varchar(100) not null,
                    url varchar(100) not null,
                    vote_up varchar(10) not null);''')
conn.commit()
conn.close()