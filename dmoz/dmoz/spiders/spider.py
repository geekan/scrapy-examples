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


from dmoz.items import *
from misc.log import *
from misc.spider import CommonSpider


class dmozSpider(CommonSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.com"]
    start_urls = [
        "http://www.dmoz.com/",
    ]
    rules = [
        Rule(sle(allow=("/topsites/category;?[0-9]*/Top/World/Chinese_Simplified_CN/.*$")), callback='parse', follow=True),
    ]

    def parse(self, response):
        info('Parse '+response.url)
