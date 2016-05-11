#coding:utf-8

'''
This tutorial include several spiders:
    page_recorder
    dmoz_item
    douban_book
'''


import re
from urlparse import urljoin


from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy import log
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from tutorial.items import TutorialItem
from tutorial.misc.log import *


class PageRecorderSpider(Spider):
    '''
    Download resources from start_urls.
    '''
    name = 'page_recorder'
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)


class DmozItemSpider(Spider):
    name = "dmoz_item"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        items = []
        for site in sites:
            item = TutorialItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
        return items


class DoubanBookTagSpider(Spider):
    name = "douban_tag_book"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://book.douban.com/tag/"
    ]
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
        return -1

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//tr/td')
        items = []
        info('url:' + response.url +
             ' depth:' + str(self._cal_depth(response)))
        for site in sites:
            item = TutorialItem()
            item['title'] = site.xpath('a/text()').extract()
            base_url = get_base_url(response)
            relative_url = site.xpath('a/@href').extract()
            item['link'] = [urljoin(base_url, u) for u in relative_url]
            item['num'] = site.xpath('b/text()').extract()
            #print repr(item).decode("unicode-escape")

            items.append(item)
        return items


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

    '''
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//tr/td')
        items = []
        info('url:' + response.url +
             ' depth:' + str(self._cal_depth(response)))
        for site in sites:
            item = TutorialItem()
            item['title'] = site.xpath('a/text()').extract()
            base_url = get_base_url(response)
            relative_url = site.xpath('a/@href').extract()
            item['link'] = [urljoin(base_url, u) for u in relative_url]
            item['num'] = site.xpath('b/text()').extract()
            #print repr(item).decode("unicode-escape")

            items.append(item)
        return items
    '''
