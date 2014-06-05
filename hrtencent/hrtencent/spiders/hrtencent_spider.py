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


from hrtencent.items import *
from misc.log import *


class HrtencentSpider(CrawlSpider):
    name = "hrtencent"
    allowed_domains = ["tencent.com"]
    start_urls = [
        "http://hr.tencent.com/position.php?start=%d" % d for d in range(0, 20, 10)
    ]
    rules = [
        Rule(sle(allow=("/position_detail.php\?id=\d*.*", )), callback='parse_2'),
        Rule(sle(allow=("/position.php\?&start=\d{,2}#a")), follow=True, callback='parse_1')
    ]

    def parse_2(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('.tablelist')
        for site in sites:
            item = PositionDetailItem()
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
