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
        Rule(sle(allow=(".*[0-9]{8}.*htm$")), callback='parse_1', follow=True),
    ]

    list_css_rules = { 
        '.linkto': {
            'url': 'a::attr(href)',
            'name': 'a::text',
        }   
    }

    list_css_rules_2 = {
        '#listZone .Q-tpWrap': {
            'url': '.linkto::attr(href)',
            'name': '.linkto::text'
        }
    }

    content_css_rules = {
        'text': '#Cnt-Main-Article-QQ p *::text',
        'images': '#Cnt-Main-Article-QQ img::attr(src)',
        'images-desc': '#Cnt-Main-Article-QQ div p+ p::text',
    }

    def parse_0(self, response):
        info('Parse0 '+response.url)
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        pp.pprint(x)
        #return self.parse_with_rules(response, self.list_css_rules, qqnewsItem)

    def parse_1(self, response):
        info('Parse1 '+response.url)
        x = self.parse_with_rules(response, self.content_css_rules, dict)
        pp.pprint(x)
        #import pdb; pdb.set_trace()

    def parse_2(self, response):
        info('Parse2 '+response.url)

