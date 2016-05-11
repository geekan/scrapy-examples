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


from amazonbook.items import *
from misc.log import *
from misc.spider import CommonSpider


import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
pp = MyPrettyPrinter()


class amazonbookSpider(CommonSpider):
    name = "amazonbook"
    allowed_domains = ["amazon.com", "www.amazon.com"]
    start_urls = [
        #"http://www.amazon.com/b/ref=s9_acss_bw_en_BGG15eve_d_1_6?_encoding=UTF8&node=17&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-top-3&pf_rd_r=0XCRZV6SDKBTKDPH8SFR&pf_rd_t=101&pf_rd_p=2293718502&pf_rd_i=283155",
        "http://www.amazon.com/books-used-books-textbooks/b?node=283155",
    ]
    rules = [
        #Rule(sle(allow=("/gp/product/.*")), callback='parse_1', follow=True),
        Rule(sle(allow=("/books-used-books-textbooks/.*")), callback='parse_0', follow=True),
    ]

    css_rules = {
        ".inner .a-row": {
            "url": ".title::attr(href)",
            #"desc": "span::text"
            "title": ".s9TitleText::text",
            "comments": ".a-icon-row .a-size-small::text",
        }
    }

    def parse_0(self, response):
        info('Parse 0 '+response.url)
        pp.pprint(self.parse_with_rules(response, self.css_rules, dict))

    #.inner .a-row
    def parse_1(self, response):
        info('Parse 1 '+response.url)
        #pp.pprint(self.parse_with_rules(response, self.css_rules, dict))
        # return self.parse_with_rules(response, self.css_rules, amazonbookItem)
