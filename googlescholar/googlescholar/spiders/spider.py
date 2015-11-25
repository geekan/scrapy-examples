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
        #"http://scholar.google.com/scholar?q=estimate+ctr&btnG=&hl=en&as_sdt=0%2C5&as_ylo=2011",
        #"http://scholar.google.com",
    ]
    rules = [
        Rule(sle(allow=("scholar\?.*")), callback='parse_1', follow=False),
    ]

    list_css_rules = {
        '.gs_ri': {
            'title': '.gs_rt a *::text',
            'url': '.gs_rt a::attr(href)',
            'pdf-text': '.gs_md_wp a *::text',
            'pdf-url': '.gs_md_wp a::attr(href)',
            'citation-text': '.gs_fl > a:nth-child(1)::text',
            'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, googlescholarItem)
