import re
import json
from urlparse import urlparse
import urllib
import pdb


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from googlescholar.items import *
from misc.log import *
from misc.spider import CommonSpider


class googlescholarSpider(CommonSpider):
    name = "googlescholar"
    allowed_domains = ["google.com"]
    start_urls = [
        "http://scholar.google.com/scholar?as_ylo=2011&q=machine+learning&hl=en&as_sdt=0,5",
        "http://scholar.google.com/scholar?q=estimate+ctr&btnG=&hl=en&as_sdt=0%2C5&as_ylo=2011"
    ]
    rules = [
        Rule(sle(allow=(".*")), callback='parse_1', follow=False),
    ]

    def parse_1(self, response):
        info('Parse '+response.url)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        # pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, googlescholarItem)
