import re
import json


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from sis.items import *
from sis.misc.log import *


class sisSpider(CrawlSpider):
    name = "sis"
    allowed_domains = ["tencent.com"]
    start_urls = [
        "http://38.103.161.147/forum/forum-%d-1.html" % d for d in [143, 230]
    ]
    rules = [
        # Rule(sle(allow=("/position_detail.php\?id=\d*.*", )), callback='parse_2'),
        Rule(sle(allow=("/forum/thread-\d*-1-1.html")), callback='parse_1'),
        Rule(sle(allow=("/forum/forum-\d*-1.html")), follow=True, callback='parse_1', process_request='_process_request'),
    ]

    def parse_2(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('.tablelist')
        for site in sites:
            item = SisItem()
            item['sharetitle'] = site.css('.h #sharetitle::text').extract()
            item['bottomline'] = site.css('.bottomline td::text').extract()
            # item['duty'] = site.css('.c .l2::text').extract()
            item['link'] = response.url
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'
        # info('parsed ' + str(response))
        self.parse_1(response)
        return items

    def parse_1(self, response):
        # url cannot encode to Chinese easily.. XXX
        info('parsed ' + str(response))

    def _process_request(self, request):
        info('process ' + str(request))
        return request
