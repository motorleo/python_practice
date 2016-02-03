#!/usr/bin/python
# -*- coding: utf-8 -*-

from sets import Set
import logging
import cookielib
import urllib
import urllib2

class ZhihuChannel:
    def __init__(self,queue,email,password):
        cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cookie)
        proxy_handler = urllib2.ProxyHandler({'http':'1.60.158.220:9000'})
        self.opener = urllib2.build_opener(cookie_handler,proxy_handler)
        logindata = urllib.urlencode({
            "_xsrf":"2cec849bfdc0744a4936d508a2a6d16b",
            "password":password,
            "remember_me":"true",
            "email":email
            })
        response = self.opener.open('https://www.zhihu.com/login/email',logindata)
        if response is None:
            logging.warning('Error Loginning.')
            exit()
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
        self.queue = queue
        self.urlSet = Set()
        self.topicSet = Set()
        self.exiting = False

    def getOpen(self,url):
        request = urllib2.Request(url,headers=self.headers)
        try:
            response = self.opener.open(request)
        except urllib2.HTTPError, e:
            logging.info('{} :Error opening URL:{}'.format(e.code,url))
            return None
        except urllib2.URLError, e:
            logging.info('{}  {} :Error opening URL:{}'.format(e.code,e.reason,url))
            return None
        else:
            logging.info('Successfully opened URL:{}'.format(url))
            return response

    def postOpen(self,url,data):
        request = urllib2.Request(url,data,self.headers)
        try:
            response = self.opener.open(request)
        except urllib2.HTTPError, e:
            logging.info('{}'.format(e.code))
            return None
        except urllib2.URLError, e:
            logging.info('{}  {} :Error posting URL:{}'.format(e.code,e.reason,url))
            return None
        else:
            logging.info('Successfully post URL:{}'.format(url))
            return response

       
