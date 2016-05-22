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


from meijutt.items import *
from misc.log import *
from misc.spider import CommonSpider


class meijuttSpider(CommonSpider):
    name = "meijutt"
    allowed_domains = ["meijutt.com"]
    start_urls = [
        "http://www.meijutt.com/content/meiju117.html", # 3
        "http://www.meijutt.com/content/meiju116.html", # 4
    ]
    rules = [
        Rule(sle(allow=(".*meiju11[67]\.html$")), callback='parse_1', follow=False),
    ]

    content_css_rules = {
        '.downurl .adds': {
            'links': 'input::attr(value)'
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        x = self.parse_with_rules(response, self.content_css_rules, dict)
        pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, meijuttItem)
