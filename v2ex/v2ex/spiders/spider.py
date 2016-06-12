import re
import json
from urlparse import urlparse
import urllib
import pdb


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from v2ex.items import *
from misc.log import *
from misc.spider import CommonSpider


class v2exSpider(CommonSpider):
    name = "v2ex"
    allowed_domains = ["v2ex.com"]
    start_urls = [
        "http://www.v2ex.com/",
    ]
    rules = [
        Rule(sle(allow=("http://www.v2ex.com/$")), callback='parse_1', follow=True),
    ]

    list_css_rules = { 
        '.cell.item': {
            'title': '.item_title a::text',
            'node': '.node::text',
            'author': '.node+ strong a::text',
            'reply_count': '.count_livid::text'
        }   
    }   

    def parse_1(self, response):
        info('Parse '+response.url)
        # import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        print(json.dumps(x, ensure_ascii=False, indent=2))
        #pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, v2exItem)
