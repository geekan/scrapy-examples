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


from arxiv.items import *
from misc.log import *
from misc.spider import CommonSpider


class arxivSpider(CommonSpider):
    name = "arxiv"
    allowed_domains = ["arxiv.org"]
    start_urls = [
        'http://arxiv.org/corr/home',
    ]
    rules = [
        Rule(sle(allow=('http://arxiv\.org/list/cs.{3}/recent')), callback='parse_1', follow=True),
    ]

    #'http://export.arxiv.org/api/query?search_query=all:Artificial%20Intelligence&start=0&max_results=10'

    def parse_1(self, response):
        info('Parse '+response.url)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        # pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, arxivItem)
