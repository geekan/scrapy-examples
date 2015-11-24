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


from template.items import *
from misc.log import *
from misc.spider import CommonSpider


class templateSpider(CommonSpider):
    name = "template"
    allowed_domains = ["template.com"]
    start_urls = [
        "http://www.template.com/",
    ]
    rules = [
        Rule(sle(allow=("/topsites/category;?[0-9]*/Top/World/Chinese_Simplified_CN/.*$")), callback='parse_1', follow=True),
    ]

    def parse_1(self, response):
        info('Parse '+response.url)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        # pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, templateItem)
