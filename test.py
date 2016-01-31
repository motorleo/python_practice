#!/usr/bin/python
# -*- coding: utf-8 -*-

from sets import Set
import sys
import cookielib
import urllib
import urllib2
import re
import sqlite3
from bs4 import BeautifulSoup

class Zhihu:
    def __init__(self):
        loginUrl = 'https://www.zhihu.com/login/email'
        cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPCookieProcessor(cookie))
        password = ''
        email = ''
        logindata = urllib.urlencode({
            "_xsrf":"2cec849bfdc0744a4936d508a2a6d16b",
            "password":'llc372101',
            "remember_me":"true",
            "email":'79174971@qq.com'
            })
        response = self.opener.open(loginUrl,logindata)
        print response.read().decode('unicode-escape')
        self.headers = {"Accept":"*/*",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "cookie":cookie,
            "Host":"www.zhihu.com",
            "Origin":"https://www.zhihu.com",
            "Referer":"https://www.zhihu.com/",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
            }
        self.topicsUrl = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
 
    def getID(self):
        request = urllib2.Request('https://www.zhihu.com/topics',
                headers=self.headers)
        response = self.opener.open(request)
        IDsoup = BeautifulSoup(response.read())
        self.ID = IDsoup.find('ul',
                class_='zm-topic-cat-main clearfix').find_all('li')

    def getTopics(self,ID):
        hasmore = True
        offset = 0
        while hasmore:
            params = ('''{
                    "topic_id":%s,
                    "offset":%d,
                    "hash_id":"93c19ac70419d81ede4a80676ae4842b"}'''%(ID['data-id'],offset)
                    )
            offset += 20
            data = urllib.urlencode(
                {"method":'next',
                'params':params,
                '_xsrf':'2cec849bfdc0744a4936d508a2a6d16b'})
            request = urllib2.Request(self.topicsUrl,data,self.headers)
            #get tags
            try:
                result = self.opener.open(request)
            except urllib2.URLError, e:
                if hasattr(e,"code"):
                    print e.code
                if hasattr(e,"reason"):
                    print e.reason
                break
            soup = BeautifulSoup(result.read().decode("unicode-escape"))
            tags = soup.find_all('div',class_='item')
            if len(tags) != 20:
                hasmore = False
            #do datamine(for each tag)
            for tag in tags:
                self.datamine(tag)

    def datamine(self,tag):
        nextPage = True
        pageHref = tag.a['href'].replace('\\','')
        pagenum = 1
        pageUrl = 'https://www.zhihu.com' + pageHref + '/top-answers'
        #for each page
        while nextPage:
            try:
                page = self.opener.open(pageUrl)
            except urllib2.URLError, e:
                if hasattr(e,"code"):
                    print e.code
                if hasattr(e,"reason"):
                    print e.reason
                break
            pagenum += 1
            pageUrl = ('https://www.zhihu.com' + 
                      pageHref + '/top-answers?page=%d'%(pagenum))
            soup = BeautifulSoup(page.read())
            #for each question
            for item in soup.find_all('div',class_='feed-main'):
                question = item.h2.a.string
                print question
                vote_up = item.find('span',class_='count').string
                if 'K' not in vote_up:
                    print vote_up,u'丢弃'
                    nextPage = False
                    break
                else:
                    print vote_up
                href = item.find('div',class_='zm-item-rich-text')
                href = href['data-entry-url'].replace('\\','')
                print href
                if href in self.urlset:
                    print u'重复丢弃'
                    continue
                else:
                    self.urlset.add(href)
                self.conn.execute('''insert into zhihu
                                values('%s','%s','%s');'''%(question,href,vote_up))
                self.conn.commit()
                print ('Successfully saved!')

    def start(self):
        self.conn = sqlite3.connect('zhihu.db')
        self.urlset = Set()
        self.getID()
        for topicID in self.ID:
            self.getTopics(topicID)
        self.conn.close()
        pass

zhihu = Zhihu()
zhihu.start()
