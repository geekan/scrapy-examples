import re
import json


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from qqnews.items import *
from misc.log import *
from misc.spider import CommonSpider


class qqnewsSpider(CommonSpider):
    name = "qqnews"
    allowed_domains = ["tencent.com", 'qq.com']
    start_urls = [
        'http://news.qq.com/society_index.shtml'
    ]
    rules = [
        Rule(sle(allow=('society_index.shtml')), callback='parse_0', follow=True),
        #Rule(sle(allow=(".*htm.*")), callback='parse_1', follow=True),
    ]
    list_css_rules = { 
        '.linkto': {
            'url': 'a::attr(href)',
            'name': 'a::text',
        }   
    }

    def parse_0(self, response):
        info('Parse0 '+response.url)
        return self.parse_with_rules(response, self.list_css_rules, qqnewsItem)

    def parse_1(self, response):
        info('Parse1 '+response.url)

    def parse_2(self, response):
        info('Parse2 '+response.url)

