# -*- coding: utf-8 -*-
import requests
from scrapy.http import Request
from scrapy.selector import Selector

try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

from misc.spider import CommonSpider

BAIDU_GEO = u'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=gQsCAgCrWsuN99ggSIjGn5nO'


class dianpingSpider(CommonSpider):
    name = "dianping"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://www.dianping.com/search/category/2/30/g141r1471", #足疗按摩
        "http://www.dianping.com/search/category/2/30/g140r1471", #洗浴
        "http://www.dianping.com/search/category/2/30/g2827r1471", #中医养生


    ]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class="tit"]/a/@href').extract()
        for site in sites:
            if site.startswith('/shop/'):
                yield Request("http://www.dianping.com{}".format(site), callback=self.parse_shop)

    def parse_shop(self, response):
        shop = {}
        hxs = Selector(response)
        shop_name = hxs.css('.shop-name::text').extract_first().strip()
        shop['name'] = shop_name
        address = hxs.css('.address span.item::text').extract_first().strip()
        shop['address'] = address
        phone_number = hxs.css('.tel span.item::text').extract_first().strip()
        shop['phone_number'] = phone_number
        path = u'//span[contains(text(), "营业时间：")]/following-sibling::span/text()'
        opening_hours = hxs.xpath(path).extract_first().strip()
        shop['opening_hours'] = opening_hours
        data = requests.get(BAIDU_GEO.format(address)).json()
        shop['longitude'] = data['result']['location']['lng']
        shop['latitude'] = data['result']['location']['lat']
        store_images = hxs.xpath("//div[@class='photos-container']//img/@src").extract()
        shop['store_images'] = ','.join(store_images[:2])
        deals = hxs.xpath("//div[@id='sales']//a/@href").extract()
        shop['deals'] = deals
        return shop


class dianpingDealSpider(CommonSpider):
    name = "dianping-deal"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://t.dianping.com/deal/21481263",

    ]

    def parse(self, response):
        hxs = Selector(response)
        name = hxs.xpath('//div[@class="bd"]/h1/text()').extract_first()
        name = name.replace(' ', '').replace('\n', '')
        print name
