import re
import json
from urlparse import urlparse
import urllib


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from dmoz.items import *
from misc.log import *
from misc.spider import CommonSpider


class dmozSpider(CommonSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/",
    ]
    valid_categories = [
        'Arts', 'Business', 'Computers', 'Games', 'Health', 'Home',
        'Kids_and_Teens', 'News', 'Recreation', 'Reference', 'Regional', 'Science',
        'Shopping', 'Society', 'Sports',
    ]
    allow_rules = ['/'+i+'/' for i in valid_categories]
    rules = [
        Rule(sle(allow=allow_rules), callback='parse_1', follow=True),
    ]

    item_rules = {
        '.directory-url li': {
            '__use': 'dump',
            '__list': True,
            'url': 'li > a::attr(href)',
            'name': 'a::text',
            'description': 'li::text',
        }
    }

    def parse_1(self, response):
        info('Parse depth 1 '+response.url)
        items = self.parse_with_rules(response, self.item_rules, dmozItem)
        return items
