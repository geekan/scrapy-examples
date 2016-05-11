import re
import json


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from doubanbook.items import *
from misc.log import *


class DoubanBookSpider(CrawlSpider):
    name = "doubanbook"
    allowed_domains = ["douban.com"]
    start_urls = [
        "https://book.douban.com/tag/"
    ]
    rules = [
        Rule(sle(allow=("/subject/\d+$")), callback='parse_2'),
        Rule(sle(allow=("/tag/[^/]+$", )), follow=True),
        #Rule(sle(allow=("/tag/$", )), follow=True),
    ]

    def parse_2(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('#wrapper')
        for site in sites:
            item = DoubanSubjectItem()
            item['title'] = site.css('h1 span::text').extract()
            item['link'] = response.url
            item['content_intro'] = site.css('#link-report .intro p::text').extract()
            items.append(item)
            # print repr(item).decode("unicode-escape") + '\n'
            print item
        # info('parsed ' + str(response))
        return items

    def parse_1(self, response):
        # url cannot encode to Chinese easily.. XXX
        info('parsed ' + str(response))

    def process_request(self, request):
        info('process ' + str(request))
        return request

    def closed(self, reason):
        info("DoubanBookSpider Closed:" + reason)
