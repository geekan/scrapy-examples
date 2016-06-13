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


from pandatv.items import *
from misc.log import *
from misc.spider import CommonSpider


class pandatvSpider(CommonSpider):
    name = "pandatv"
    allowed_domains = ["panda.tv"]
    start_urls = [
        "http://www.panda.tv/all",
    ]
    rules = [
        Rule(sle(allow=("http://www.panda.tv/all")), callback='parse_1', follow=True),
    ]

    list_css_rules = { 
        '.video-list-item.video-no-tag': {
            'room_name': '.video-title::text',
            'author': '.video-nickname::text',
            'people_count': '.video-number::text',
            'tag': '.video-cate::text',
        }   
    }   

    content_css_rules = { 
        'text': '#Cnt-Main-Article-QQ p *::text',
        'images': '#Cnt-Main-Article-QQ img::attr(src)',
        'images-desc': '#Cnt-Main-Article-QQ div p+ p::text',
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        print(json.dumps(x, ensure_ascii=False, indent=2))
        # pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, pandatvItem)
