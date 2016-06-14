# encoding:utf8
"""
zhibo8直播源解密
"""
import scrapy
import sys
import re 
import urllib2
reload(sys)
sys.setdefaultencoding( "utf-8" )

test_url = 'http://zhibo8.cc/zhibo/zuqiu/2016/0203laisitechengvsliwupu.htm'

class Zhibo8Decrypt():

   def get_content(self, url, send_headers=''):
       send_headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'}
       req = urllib2.Request(url, headers=send_headers)
       ret = urllib2.urlopen(req)
       html = ret.read()
       return html

   def decrypt(self, content):
        if '' == content:
            return '' 
        pattern = re.compile(r'C0ha0ne0l(.*?)')
        ch = pattern.findall(content)
        return ch


zd = Zhibo8Decrypt()
content = zd.get_content(test_url)
zd.decrypt(content)
