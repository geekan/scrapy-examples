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


from proxylist.items import *
from misc.log import *
from misc.spider import CommonSpider


class proxylistSpider(CommonSpider):
    name = "proxylist"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = [
        "https://free-proxy-list.net/",
    ]
    rules = [
        Rule(sle(allow=("/")), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        'tbody tr': {
            'ip': 'td:nth-child(1)::text',
            'port': 'td:nth-child(2)::text',
            'code': 'td:nth-child(3)::text',
            'country': 'td:nth-child(4)::text',
            'anonymity': 'td:nth-child(5)::text',
            'google': 'td:nth-child(6)::text',
            'https': 'td:nth-child(7)::text',
            'last-checked': 'td:nth-child(8)::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        sel = Selector(response)
        #import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        pp.pprint(x['tbody tr'])
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)
