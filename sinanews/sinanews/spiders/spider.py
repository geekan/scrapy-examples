import re
import json
from urlparse import urlparse
import urllib


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from sinanews.items import *
from misc.log import *
from misc.spider import CommonSpider


class sinanewsSpider(CommonSpider):
    name = "sinanews"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = [
        "http://news.sina.com.cn/",
    ]
    rules = [
        Rule(sle(allow=("http://news.sina.com.cn/$")), callback='parse_0'),
        #Rule(sle(allow=("/.*doc.*")), callback='parse_1', follow=True, process_request='process_request'),
        #Rule(sle(allow=('/c/2015-11-19/doc-ifxkszhk0386278.shtml')), callback='parse_1', follow=True, process_request='process_request'),
    ]

    list_css_rules = {
        '#blk_yw_01 a': {
            '__use': 'dump',
            '__list': True,
            'url': 'a::attr(href)',
            'name': 'a::text',
        }
    }

    def process_request(self, r):
        info('process ' + str(r))
        return r
    
    def parse_0(self, response):
        info('Parse 0 '+response.url)
        return self.parse_with_rules(response, self.list_css_rules, sinanewsItem)

    def parse_1(self, response):
        info('Parse xxx '+response.url)
        # self.parse_with_rules(response, self.css_rules, sinanewsItem)
