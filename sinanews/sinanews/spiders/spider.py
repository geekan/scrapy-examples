import re
import json
from urlparse import urlparse
import urllib
import pdb


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from sinanews.items import *
from misc.log import *
from misc.spider import CommonSpider


import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
pp = MyPrettyPrinter()


class sinanewsSpider(CommonSpider):
    name = "sinanews"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = [
        "http://news.sina.com.cn/",
    ]
    rules = [
        Rule(sle(allow=("http://news.sina.com.cn/$")), callback='parse_0'),
        Rule(sle(allow=(".*doc[^/]*shtml$")), callback='parse_1'), #, follow=True),
        #Rule(sle(allow=('/c/2015-11-19/doc-ifxkszhk0386278.shtml')), callback='parse_1', follow=True, process_request='process_request'),
    ]

    list_css_rules = {
        '#blk_yw_01 a': {
            'url': 'a::attr(href)',
            'name': 'a::text',
        }
    }

    content_css_rules = {
        'text': 'p::text',
        'images': 'img::attr(src)',
        'images-desc': '.img_descr::text',
        # need url analysis for video
        #'video': '#J_Article_Player',
    }

    def process_request(self, r):
        info('process '+str(r))
        return r
    
    def parse_0(self, response):
        info('Parse 0 '+response.url)
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        pp.pprint(x)
        #pdb.set_trace()
        #return self.parse_with_rules(response, self.list_css_rules, sinanewsItem)

    def parse_1(self, response):
        info('Parse 1 '+response.url)
        x = self.parse_with_rules(response, self.content_css_rules, dict)
        pp.pprint(x)
        #self.parse_with_rules(response, self.css_rules, sinanewsItem)
