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


from zhihu.items import *
from misc.log import *


class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        "http://www.zhihu.com/",
        "http://www.zhihu.com/people/jia-yang-qing-74",
    ]
    rules = [
        Rule(sle(allow=("/people/[^/]+/followees$")), callback='parse_followees'),
        Rule(sle(allow=("/people/[^/]+/followers$", )), callback='parse_followers'),
        Rule(sle(allow=("/people/[^/]+$", )), callback='parse_people', follow=True),
    ]

    def parse_followers(self, response):
        pass

    def parse_followees(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('#wrapper')
        for site in sites:
            item = ZhihuPeopleItem()
            item['title'] = site.css('h1 span::text').extract()
            item['link'] = response.url
            item['content_intro'] = site.css('#link-report .intro p::text').extract()
            items.append(item)
            print repr(item).decode("unicode-escape") + '\n'
        # info('parsed ' + str(response))
        return items

    def parse_people(self, response):
        info('parsed ' + str(response))
        items = []
        sel = Selector(response)
        profile_header = sel.css('.zm-profile-header')[0]
        profile_header_main = profile_header.css('.zm-profile-header-main')[0]
        profile_header_operation = profile_header.css('.zm-profile-header-operation')[0]
        profile_header_navbar = profile_header.css('.profile-navbar')[0]

        item = ZhihuPeopleItem()
        item['name'] = [i.extract() for i in profile_header_main.css('.title-section .name::text')]
        item['sign'] = [i.extract() for i in profile_header_main.css('.title-section .bio::text')]
        item['location'] = [i.extract() for i in profile_header_main.css('.location.item::text')]
        item['business'] = [i.extract() for i in profile_header_main.css('.business.item::text')]
        item['employment'] = [i.extract() for i in profile_header_main.css('.employment.item::text')]
        item['position'] = [i.extract() for i in profile_header_main.css('.position.item::text')]
        item['education'] = [i.extract() for i in profile_header_main.css('.education.item::text')]
        item['education_extra'] = [i.extract() for i in profile_header_main.css('.education-extra.item::attr(title)')]

        items.append(item)
        # import pdb; pdb.set_trace()

        return items

    def _process_request(self, request):
        info('process ' + str(request))
        return request
