import re

from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from doubanbook.items import DoubanbookItem
from doubanbook.misc.log import *


class DoubanBookSpider(CrawlSpider):
    name = "douban_book"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://book.douban.com/tag/"
    ]

    rules = (
        Rule(sle(allow=("/tag/[^/]+/?$", )), callback="parse_1"),
        Rule(sle(allow=("/tag/$", )), follow=True, process_request='_process_request'),
    )

    # NOTE: depth index is hidden.
    depth_class_list = [
        '.*/tag/?$',
        '.*/tag/.+/?',
    ]

    def _cal_depth(self, response):
        """
        Calculate the depth of response, and call corresponding method or stop
        crawl.
        """
        url = response.url
        for depth, depth_regexp in enumerate(self.depth_class_list):
            if re.match(depth_regexp, url):
                return depth
        # warn("Unknown url depth: " + url)
        # If the url pattern is unknown, then return -1.
        return -1

    def parse_1(self, response):
        # url cannot encode to Chinese easily.. XXX
        info('parsed ' + str(response))

    def _process_request(self, request):
        info('process ' + str(request))
        return request
