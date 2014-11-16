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
        Rule(sle(allow=("/[^/]*/?$")), callback='parse_1', follow=True),
        Rule(sle(allow=("/")), callback='parse_2', follow=True),
    ]
    valid_catogories = [
        'Arts', 'Business', 'Computers', 'Games', 'Health', 'Home',
        'Kids_and_Teens', 'News', 'Recreation', 'Reference', 'Regional', 'Science',
        'Shopping', 'Society', 'Sports',
    ]

    depth_1_rules = {}
    depth_2_rules = {
        '.directory-url li': {
            '__use': 'dump',
            'url': 'a::attr(href)',
            'name': 'a::text',
            'description': 'li::text',
        }
    }
    depth_3_rules = {}

    def parse_1(self, response):
        info('Parse depth 1 '+response.url)

    def parse_2(self, response):
        if urlparse(response.url).path.split('/')[0] not in valid_categories:
            return
        info('Parse depth 2 '+response.url)
