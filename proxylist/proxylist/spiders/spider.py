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
from scrapy.linkextractors import LinkExtractor as sle


from proxylist.items import *
from misc.log import *
from misc.spider import CommonSpider


class proxylistSpider(CommonSpider):
    name = "proxylist"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = [
        "https://free-proxy-list.net/",
    ]
    rules = [
        Rule(sle(allow=("/$")), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        'tbody tr': {
            'ip': 'td:nth-child(1)::text',
            'port': 'td:nth-child(2)::text',
            'code': 'td:nth-child(3)::text',
            'country': 'td:nth-child(4)::text',
            'anonymity': 'td:nth-child(5)::text',
            'google': 'td:nth-child(6)::text',
            'https': 'td:nth-child(7)::text',
            'last_checked': 'td:nth-child(8)::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        items = []
        #sel = Selector(response)
        x = self.parse_with_rules(response, self.list_css_rules, dict, True)
        x = x[0]['tbody tr']
        pp.pprint(x)
        for i in x:
            item = freeProxyListItem()
            for k, v in i.items():
                item[k] = v
            items.append(item)
        return items
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)


class hidemyassSpider(CommonSpider):
    name = "hidemyass"
    allowed_domains = ["hidemyass.com"]
    start_urls = [
        "http://proxylist.hidemyass.com",
    ]
    rules = [
        Rule(sle(allow=("/[0-9](#.*)?$")), callback='parse_1', follow=True),
    ]

    # xpath: note that the paras are not rendered, so we cannot use it directly
    # we should 1. render it or 2. write some logic to filter the real displayed node.
    # n[2].css('td:nth-child(2)').xpath(".//*[not(contains(@style,'display:none'))]/text()")
    list_css_rules = {
        'tbody tr': {
            'ip': "td:nth-child(2)", #, "xpath:.//*[not(contains(@style,'display:none'))]/text()"],
            'port': 'td:nth-child(3)::text',
            'code': 'td:nth-child(8)::text',
            'country': 'td:nth-child(4)::text',
            'speed': 'td:nth-child(5) *::attr(value)',
            'connection_time': 'td:nth-child(6) *::attr(value)',
            'type': 'td:nth-child(7)::text',
            'last_checked': '.timestamp span::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        items = []
        n = response.css('tbody tr')
        import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict, True)
        x = x[0]['tbody tr']
        pp.pprint(x)
        #for i in x:
        #    item = freeProxyListItem()
        #    for k, v in i.items():
        #        item[k] = v
        #    items.append(item)
        #return items
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)


# http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=ssl&country=&latency=1000&reliability=9000&sort=reliability&desc=true&pnum=0#table
# http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=ssl&country=&latency=1000&reliability=9000&sort=reliability&desc=true&pnum=1#table
# http://www.xroxy.com/proxylist.php?port=&type=All_http&ssl=ssl&country=&latency=1000&reliability=9000&sort=reliability&desc=true&pnum=2#table
class xroxySpider(CommonSpider):
    name = "xroxy"
    allowed_domains = ["xroxy.com"]
    start_urls = [
        "http://xroxy.com/proxylist.php?port=&type=All_http&ssl=ssl&country=&latency=1000&reliability=9000&sort=reliability&desc=true&pnum=0#table",
    ]
    rules = [
        Rule(sle(allow=("/proxylist.php\?port=&type=All_http&ssl=ssl&country=&latency=1000&reliability=9000&sort=reliability&desc=true&pnum=[0-9]+#table$")), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        'tbody tr': {
            'ip': "td:nth-child(2) a::text", #, "xpath:.//*[not(contains(@style,'display:none'))]/text()"],
            'port': 'td:nth-child(3) a::text',
            'type': 'td:nth-child(4) a::text',
            'country': 'td:nth-child(6) a::text',
            'latency': 'td:nth-child(7)::text',
            'reliability': 'td:nth-child(8)::text',
            'detail': 'td:nth-child(9) a::attr(href)',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        items = []
        n = response.css('tbody tr')
        import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict, True)
        x = x[0]['tbody tr']
        pp.pprint(x)
        #for i in x:
        #    item = freeProxyListItem()
        #    for k, v in i.items():
        #        item[k] = v
        #    items.append(item)
        #return items
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)


class samairSpider(CommonSpider):
    name = "samair"
    allowed_domains = ["samair.ru"]
    start_urls = [
        'http://www.samair.ru/proxy/'
    ]
    rules = [
        Rule(sle(allow=("proxy/$")), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        '#proxylist tr': {
            'ip': "td:nth-child(1) *::text", #, "xpath:.//*[not(contains(@style,'display:none'))]/text()"],
            #'port': 'td:nth-child(3) a::text',
            'anonymity': 'td:nth-child(2) *::text',
            'last_checked': 'td:nth-child(3) *::text',
            'country': 'td:nth-child(4) a::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        items = []
        n = response.css('tbody tr')
        #import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict, True)
        x = x[0]['#proxylist tr']
        pp.pprint(x)
        #for i in x:
        #    item = freeProxyListItem()
        #    for k, v in i.items():
        #        item[k] = v
        #    items.append(item)
        #return items
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)


class proxylistorgSpider(CommonSpider):
    name = "proxylistorg"
    allowed_domains = ["proxy-list.org"]
    start_urls = [
        'https://proxy-list.org/english/index.php'
    ]
    rules = [
        Rule(sle(allow=("english/index.php(\?p=[0-9]+)?$")), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        '#proxy-table .table ul': {
            'ip': "li:nth-child(1)::text", #, "xpath:.//*[not(contains(@style,'display:none'))]/text()"],
            #'port': 'td:nth-child(3) a::text',
            'anonymity': 'li:nth-child(4)::text',
            'speed': 'li:nth-child(3)::text',
            'ssl': 'li:nth-child(2)::text',
            'country': 'li:nth-child(5) *::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        items = []
        n = response.css('tbody tr')
        #import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict, True)
        x = x[0]['#proxy-table .table ul']
        pp.pprint(x)
        #for i in x:
        #    item = freeProxyListItem()
        #    for k, v in i.items():
        #        item[k] = v
        #    items.append(item)
        #return items
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)


class proxy4freeSpider(CommonSpider):
    name = "proxy4free"
    allowed_domains = ["proxy4free.com"]
    start_urls = [
        'http://www.proxy4free.com/list/webproxy1.html'
    ]
    rules = [
        Rule(sle(allow=("list/webproxy[0-9]+\.html")), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        'tbody tr': {
            'domain': "td:nth-child(2) *::text", #, "xpath:.//*[not(contains(@style,'display:none'))]/text()"],
            #'port': 'td:nth-child(3) a::text',
            'country': 'td:nth-child(4) *::text',
            'rating': 'td:nth-child(5) *::text',
            'access_time': 'td:nth-child(6) *::text',
            'uptime': 'td:nth-child(7) *::text',
            'online_since': 'td:nth-child(8) *::text',
            'last_checked': 'td:nth-child(9) *::text',
            'features_hian': 'td:nth-child(10) *::text',
            'features_ssl': 'td:nth-child(11) *::text',
        }
    }

    def parse_1(self, response):
        info('Parse '+response.url)
        items = []
        n = response.css('tbody tr')
        #import pdb; pdb.set_trace()
        x = self.parse_with_rules(response, self.list_css_rules, dict, True)
        x = x[0]['tbody tr']
        pp.pprint(x)
        #for i in x:
        #    item = freeProxyListItem()
        #    for k, v in i.items():
        #        item[k] = v
        #    items.append(item)
        #return items
        # return self.parse_with_rules(response, self.css_rules, proxylistItem)


