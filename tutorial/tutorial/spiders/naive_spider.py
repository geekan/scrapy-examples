#coding:utf-8

'''
This is a naive spider only for example
'''
from scrapy.selector import Selector
from scrapy.spider import BaseSpider as Spider
from tutorial.items import TutorialItem
from scrapy.utils.response import get_base_url
from urlparse import urljoin

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


def make_absolute_url(response, relative_url):
    base_url = urlparse.urljoin(response)
    return urljoin_rfc(base_url, relative_url)


class DoubanBookSpider(Spider):
    name = "douban_book"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://book.douban.com/tag/"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//tr/td')
        items = []
        for site in sites:
            item = TutorialItem()
            item['title'] = site.xpath('a/text()').extract()
            base_url = get_base_url(response)
            relative_url = site.xpath('a/@href').extract()
            item['link'] = [urljoin(base_url, u) for u in relative_url]
            item['num'] = site.xpath('b/text()').extract()
            items.append(item)
        return items
