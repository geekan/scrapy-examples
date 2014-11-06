# coding: utf-8

import re
import json
import sys
from urlparse import urljoin


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from sis.items import *
from misc.log import *


class sisSpider(CrawlSpider):
    name = "sis"
    ip = "38.103.161.187"
    allowed_domains = [ip]
    ip_format = 'http://' + ip + '/forum/forum-%d-1.html'
    '''
    start_urls = [
        # ip_format % d for d in [230] #[143, 230, 58]
    ]
    rules = [
        # Rule(sle(allow=("/forum/thread-\d*-1-1\.html")), callback='parse_2'),
        # Rule(sle(allow=("/forum/forum-(143|230|58)-[0-9]{,2}\.html")), follow=True, callback='parse_1'),
        Rule(sle(allow=("/forum/forum-230-[0-9]{,4}\.html")), follow=True, callback='parse_1'),
    ]
    '''

    def __init__(self, forum_id=58, digit=1, *args, **kwargs):
        self.start_urls = [self.ip_format % d for d in [int(forum_id)]]
        self.rules = [Rule(sle(allow=("/forum/forum-" + forum_id + "-[0-9]{," + digit + "}\.html")), follow=True, callback='parse_1'),]
        super(sisSpider, self).__init__(*args, **kwargs)

    def parse_2(self, response):
        items = []
        sel = Selector(response)
        sites = sel.css('.postcontent')[0:1]
        for site in sites:
            item = SisItem()
            item['title'] = site.css('.postmessage h2::text').extract()
            imgs = site.css('.postmessage img::attr(src)').extract()
            item['imgs'] = filter(lambda x: not x.endswith('.gif'), imgs)
            item['torrents'] = [urljoin(response.url, x) for x in site.css('.t_attachlist a[href*=attachment]::attr(href)').extract()]
            # item['duty'] = site.css('.c .l2::text').extract()
            item['link'] = response.url
            items.append(item)
            # print repr(item).decode("unicode-escape") + '\n'
        # info('parsed ' + str(response))
        self.parse_1(response)
        return items

    def parse_1(self, response):
        items = []
        # url cannot encode to Chinese easily.. XXX
        info('parsed ' + str(response))
        sel = Selector(response)
        threads = sel.css('tbody[id*=normalthread_]')
        for thread in threads:
            item = SisForumListItem()
            # filter some thread
            inner_thread = thread.css('span[id*=thread_]')
            url = urljoin(response.url, inner_thread.css('a[href]::attr(href)').extract()[0])
            thread_content = re.sub(r"\s\s+", " ", thread.extract())
            # if re.search(u"(奸|姦)", thread_content):
            item['title'] = inner_thread.css('a::text').extract()[0]
            item['link'] = url
            item['star'] = re.sub(r'\s+', '', thread.css('td[class=author] cite::text').extract()[1])
            item['comment'] = thread.css('td[class=nums] strong::text').extract()[0]
            item['view'] = thread.css('td[class=nums] em::text').extract()[0]
            item['post_time'] = thread.css('td[class=author] em::text').extract()[0]
            print ' ', item['post_time'], item['star'], '|', item['title'], item['link'], item['comment'], item['view']

            # NOTE: content is only for debug purpose
            # item['content'] = thread_content

            items.append(item)
            # yield Request(url, callback=parse_2)
        return items

    def _process_request(self, request):
        info('process ' + str(request))
        return request
