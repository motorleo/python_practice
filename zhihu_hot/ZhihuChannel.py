#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import cookielib
import httplib
import urllib
import urllib2
import sqlite3
import threading

class ZhihuChannel:
    def __init__(self,queue,email,password):
        cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cookie)
        proxy_handler = urllib2.ProxyHandler({'http':'182.40.50.201:8090'})
        self.opener = urllib2.build_opener(cookie_handler,proxy_handler)
        logindata = urllib.urlencode({
            "_xsrf":"2cec849bfdc0744a4936d508a2a6d16b",
            "password":password,
            "remember_me":"true",
            "email":email
            })
        response = self.opener.open('https://www.zhihu.com/login/email',logindata)
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
        self.exiting = False
        self.makeSet()
        self.answerSetLock = threading.Lock()
        self.answerSaveLock = threading.Lock()
        self.tagSetLock = threading.Lock()
        self.tagSaveLock = threading.Lock()

    def getOpen(self,url):
        logging.info('Opening URL:{}'.format(url))
        request = urllib2.Request(url,headers=self.headers)
        try:
            response = self.opener.open(request,timeout=3).read()
        except urllib2.URLError as e:
            message = ''
            if hasattr(e,"code"):
                message += str(e.code) +' '
            if hasattr(e,"reason"):
                message += str(e.reason)
            logging.info('{} :Error opening URL:{}'.format(message,url))
            return None
        except httplib.IncompleteRead as e:
            logging.info('IncompleteRead Exception.')
            response = e.partial
            return response
        except Exception as e:
            logging.info('Unknow Error opening URL:{}'.format(url))
            return None
        else:
            logging.info('Successfully opened URL:{}'.format(url))
            return response

    def postOpen(self,url,data):
        request = urllib2.Request(url,data,self.headers)
        try:
            response = self.opener.open(request,timeout=3).read()
        except urllib2.URLError as e:
            message = ''
            if hasattr(e,"code"):
                message += str(e.code) +' '
            if hasattr(e,"reason"):
                message += str(e.reason)
            logging.info('{} :Error posting URL:{}'.format(message,url))
            return None
        except httplib.IncompleteRead as e:
            logging.info('IncompleteRead Exception.')
            response = e.partial
            return response
        except Exception as e:
            logging.info('Unknow Error posting URL:{}'.format(url))
            return None
        else:
            logging.info('Successfully post URL:{}'.format(url))
            return response
    
    def makeSet(self):
        #answerUrlSet
        conn = sqlite3.connect('zhihu.db')
        self.answerUrlSet = set()
        cursor = conn.execute('''select url from zhihu;''')
        for url in cursor:
            self.answerUrlSet.add(url[0])
        conn.close()
        #tagUrlSet
        conn = sqlite3.connect('tagUrlSet.db')
        self.tagUrlSet = set()
        cursor = conn.execute('''select url from tagUrlSet
                                    where checked = 1;''')
        for url in cursor:
            self.tagUrlSet.add(url[0])
        conn.close()

       
