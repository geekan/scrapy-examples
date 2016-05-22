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


from doubanmovie.items import *
from misc.log import *
from misc.spider import CommonSpider


class doubanmovieSpider(CommonSpider):
    name = "doubanmovie"
    allowed_domains = ["douban.com"]
    start_urls = [
        #"https://movie.douban.com/tag/",
        "https://movie.douban.com/chart"
    ]
    rules = [
        #Rule(sle(allow=("/tag/[0-9]{4}$")), follow=True),
        #Rule(sle(allow=("/tag/[0-9]{4}/?start=[0-9]{2,4}&type=T$")), follow=True),
        #Rule(sle(allow=("/subject/[0-9]+$")), callback='parse_1'),
        Rule(sle(allow=("/subject/[0-9]+/$")), callback='parse_1', follow=True),
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
        'rating_per': '.rating_per::text',
        'rating_num': '.rating_num::text',
        'title': 'h1 span:nth-child(1)::text',
        'rating_people': '.rating_people span::text',
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        x = self.parse_with_rules(response, self.content_css_rules, dict)
        return x
        #print(repr(x).decode('raw_unicode_escape'))
        # return self.parse_with_rules(response, self.css_rules, doubanmovieItem)
