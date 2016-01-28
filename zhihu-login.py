#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cookielib
import urllib
import urllib2
import re
from bs4 import BeautifulSoup

class Zhihu:
    def __init__(self,email,password):
        self.loginUrl = 'https://www.zhihu.com/login/email'
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.postdata = urllib.urlencode({
            "_xsrf":"2cec849bfdc0744a4936d508a2a6d16b",
            "password":password,
            "remember_me":"true",
            "email":email
        })

    def getPage(self):
        try:
            self.opener.open("https://www.zhihu.com/login/email",self.postdata)
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
            exit()
        self.result = self.opener.open("https://www.zhihu.com/")
        self.soup = BeautifulSoup(self.result.read())

    def printQuestion(self):
        for tag in self.soup.find_all('div',
                class_=['feed-item','folding','feed-item-hook']):
            if tag['data-feedtype'] == 'QUESTION_FOLLOW':
                continue
            print '-----------------------------------------------------------------'
            print '*****************************************************************'
            print '-----------------------------------------------------------------'
            follower = tag.find('div',class_='source')
            #follower
            for item in follower.stripped_strings:
                print item,
            print '\n'
            content = tag.find('div',class_='content')
            #title
            print content.h2.a.string
            #author
            if tag['data-feedtype'] == 'ANSWER_VOTE_UP':
                author = content.find('div',class_='zm-item-answer-author-info')
                for item in author.stripped_strings:
                    print item,
            print '\n'
            #context
            context = content.find('textarea')
            context = context.contents[0].strip()
            PReplace = re.compile('<img src=.*?>')
            context = re.sub(PReplace,u'\n(图)\n',context)
            PReplace = re.compile('<br>')
            context = re.sub(PReplace,'\n',context)
            PReplace = re.compile('<.*?>')
            context = re.sub(PReplace,'',context)
            print context

    def start(self):
        self.getPage()
        self.printQuestion()

if len(sys.argv) < 3:
    print 'Plaese enter the email and password.'
    exit()
zhihu = Zhihu(sys.argv[1],sys.argv[2])
zhihu.start()
