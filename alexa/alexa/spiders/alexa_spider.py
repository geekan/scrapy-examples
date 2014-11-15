import re
import json
from urlparse import urlparse
import urllib


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle


from alexa.items import *
from misc.log import *


class alexaSpider(CrawlSpider):
    name = "alexa"
    allowed_domains = ["alexa.com"]
    start_urls = [
        "http://www.alexa.com/",
        "http://www.alexa.com/topsites/category/Top",
    ]
    rules = [
        Rule(sle(allow=("/topsites/category;?[0-9]*/Top/[^/]*$")), callback='parse_category_top_xxx', follow=True),
        Rule(sle(allow=("/topsites/category/Top$", )), callback='parse_category_top', follow=True),
        #Rule(sle(allow=("/people/[^/]+$", )), callback='parse_people', follow=True),
    ]

    # www.alexa.com/topsites/category/Top/Computers
    # www.alexa.com/topsites/category;1/Top/Computers
    def parse_category_top_xxx(self, response):
        info('parsed ' + str(response))
        items = []
        sel = Selector(response)

        sites = sel.css('.site-listing')
        for site in sites:
            item = alexaSiteInfoItem()
            item['url'] = site.css('a[href*=siteinfo]::attr(href)')[0].extract()
            item['name'] = site.css('a[href*=siteinfo]::text')[0].extract()
            item['description'] = site.css('.description::text')[0].extract()
            remainder = site.css('.remainder::text')
            if remainder:
                item['description'] += remainder[0].extract()
            # more specific
            item['category'] = response.url.split('/')[-1]
            items.append(item)
        return items

    def parse_category_top(self, response):
        info('parsed ' + str(response))
        items = []
        sel = Selector(response)

        categories = sel.css('li a[href*="/topsites/category/Top/"]')
        for category in categories:
            item = alexaCategoryItem()
            item['url'] = category.css('::attr(href)')[0].extract()
            item['name'] = category.css('::text')[0].extract()
            items.append(item)
        return items


class alexaCNSpider(CrawlSpider):
    name = "alexa.cn"
    allowed_domains = ["alexa.com"]
    start_urls = [
        "http://www.alexa.com/",
        "http://www.alexa.com/topsites/category/World/Chinese_Simplified_CN",
    ]
    rules = [
        Rule(sle(allow=("/topsites/category;?[0-9]*/Top/World/Chinese_Simplified_CN/.*$")), callback='parse_category_top_xxx', follow=True),
        Rule(sle(allow=("/topsites/category/World/Chinese_Simplified_CN$", )), callback='parse_category_top_xxx', follow=True),
        #Rule(sle(allow=("/people/[^/]+$", )), callback='parse_people', follow=True),
    ]

    # www.alexa.com/topsites/category/Top/Computers
    # www.alexa.com/topsites/category;1/Top/Computers
    def parse_category_top_xxx(self, response):
        info('parsed ' + str(response))
        items = []
        sel = Selector(response)

        sites = sel.css('.site-listing')
        for site in sites:
            item = alexaSiteInfoItem()
            item['url'] = site.css('a[href*=siteinfo]::attr(href)')[0].extract()
            item['name'] = site.css('a[href*=siteinfo]::text')[0].extract()
            item['description'] = site.css('.description::text')[0].extract()
            remainder = site.css('.remainder::text')
            if remainder:
                item['description'] += remainder[0].extract()
            # more specific
            item['category'] = urllib.unquote('/'.join(response.url.split('/')[-3:])).decode('utf-8')
            items.append(item)
        return items

    def parse_category_top(self, response):
        info('parsed ' + str(response))
        items = []
        sel = Selector(response)

        categories = sel.css('li a[href*="/topsites/category/Top/"]')
        for category in categories:
            item = alexaCategoryItem()
            item['url'] = category.css('::attr(href)')[0].extract()
            item['name'] = category.css('::text')[0].extract()
            items.append(item)
        return items

