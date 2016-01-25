#!/usr/bin/python

import urllib
import urllib2
import re

def getQuestion(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        return
    content = response.read().decode("utf-8")
    PTitle = re.compile('<title>(.*?)</title>',re.S)
    PAgree = re.compile('<span class="count">(.*?)</span>',re.S)
    PContext = re.compile('<div class="zm-editable-content clearfix">(.*?)</div>',re.S)
    print re.search(PTitle,content).group(1)
    print ''
    print re.search(PAgree,content).group(1),'Person Agree.'
    context = re.search(PContext,content).group(1)
    PReplace = re.compile('<noscript>.*?</noscript><img.*?>')
    context = re.sub(PReplace,'(...)\n',context)
    PReplace = re.compile('<b>|</b>')
    context = re.sub(PReplace,'',context)
    PReplace = re.compile('<br>')
    context = re.sub(PReplace,'\n',context)
    print context

base = 'https://www.zhihu.com'
try:
    request = urllib2.Request('https://www.zhihu.com/explore')
    response = urllib2.urlopen(request)
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

content = response.read().decode("utf-8")
pattern = re.compile('<h2><a class="question_link" target="_blank" href="(.*?)">',re.S)
urls = re.findall(pattern,content)
print 'There is ',len(urls),' questions in explore.'
num = 0
for url in urls:
    num += 1
    print 'Question',num,':'
    print '\n*******************************************************\n'
    #do something
    getQuestion(base + url)
    print 'Want to see more questions?'
    print '(Empty for yes,q for exit):'
    ifExit = raw_input()
    if ifExit == 'q':
        break
print 'No more question!'
