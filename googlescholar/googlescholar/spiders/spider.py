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

    def __init__(self, start_url='', *args, **kwargs):
        if start_url:
            self.start_urls = [start_url]
        super(googlescholarSpider, self).__init__(*args, **kwargs)

    #.gs_ri: content besides related html/pdf
    list_css_rules = {
        '.gs_r': {
            'title': '.gs_rt a *::text',
            'url': '.gs_rt a::attr(href)',
            'related-text': '.gs_ggsS::text',
            'related-type': '.gs_ggsS .gs_ctg2::text',
            'related-url': '.gs_ggs a::attr(href)',
            'citation-text': '.gs_fl > a:nth-child(1)::text',
            'citation-url': '.gs_fl > a:nth-child(1)::attr(href)',
            'authors': '.gs_a a::text',
            'description': '.gs_rs *::text',
            'journal-year-src': '.gs_a::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        #sel = Selector(response)
        #v = sel.css('.gs_ggs a::attr(href)').extract()
        #import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        pp.pprint(x[0]['.gs_r'])
        # return self.parse_with_rules(response, self.css_rules, googlescholarItem)
