# -*- coding: utf-8 -*-
import requests
from json import loads
from scrapy.http import Request
from scrapy.selector import Selector

try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

from misc.spider import CommonSpider

BAIDU_GEO = u'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=gQsCAgCrWsuN99ggSIjGn5nO'

base_category_url = "http://www.dianping.com/search/category"

start_url_dict = {
    u"足疗按摩": "/2/30/g141r1471",
    u"中医养生": "/2/30/g2827r1471",
    u"健康体检": "/2/80/g612",
    u"妇幼保健": "/2/70/g258",
    u"美容Spa": "/2/50/g158",
    u"整形塑体": "/2/85/g183",
    u"运动健身": "/2/45/g147",
    u"口腔健康": "/2/85/g182",
    u"药店": "/2/85/g235"
}


def clean_string(string):
    return string.replace(' ', '').replace('\n', '') if string else ''


def address_to_geo(address):
    data = requests.get(BAIDU_GEO.format(address)).json()
    longitude = data['result']['location']['lng'] if 'result' in data else 120.260569
    latitude = data['result']['location']['lat'] if 'result' in data else 30.242865
    return {'longitude': longitude, 'latitude': latitude}


class dianpingSpider(CommonSpider):
    name = "dianping"
    allowed_domains = ["dianping.com"]

    def start_requests(self):
        for k, v in start_url_dict.items():
            for i in range(1, 3):
                url = base_category_url + v + 'p{}'.format(i)
                yield Request(url, callback=self.parse, meta={'category': k})

    def parse(self, response):
        hxs = Selector(response)
        shops = hxs.xpath('//div[@class="tit"]/a/@href').extract()
        for shop in shops:
            if shop.startswith('/shop/'):
                yield Request("http://www.dianping.com{}".format(shop), callback=self.parse_shop,
                              meta=response.request.meta)

    def parse_shop(self, response):
        shop = {}
        hxs = Selector(response)
        shop_name = hxs.css('.shop-name::text').extract_first()
        shop['name'] = clean_string(shop_name)
        address = hxs.css('.address span.item::text').extract_first()
        shop['address'] = clean_string(address)
        phone_number = hxs.css('.tel span.item::text').extract_first()
        shop['phone_number'] = clean_string(phone_number)
        path = u'//span[contains(text(), "营业时间：")]/following-sibling::span/text()'
        opening_hours = hxs.xpath(path).extract_first()
        shop['opening_hours'] = clean_string(opening_hours)
        geo = address_to_geo(address)
        shop.update(geo)
        store_images = hxs.xpath("//div[@class='photos-container']//img/@src").extract()
        shop['store_images'] = ','.join(store_images[:2])
        deals = hxs.xpath("//div[@id='sales']//a/@href").extract()
        shop['deals'] = deals
        shop['category'] = response.request.meta['category']
        return shop


class dianpingDealSpider(CommonSpider):
    name = "dianping-deal"
    allowed_domains = ["dianping.com"]

    def start_requests(self):
        with open('partner.json', 'rb') as f:
            for line in f:
                data = loads(line)
                for url in data['deals']:
                    yield Request(url, callback=self.parse, meta={'category': data['category'],
                                                                  'partner': data['name']})
                    break

    def parse(self, response):
        deal = {}
        hxs = Selector(response)
        bd = hxs.css('.bd')
        name = bd.css('.title::text').extract_first()
        deal['name'] = clean_string(name)
        description = bd.css('.sub-title span::text').extract_first()
        deal['description'] = clean_string(description)
        price = bd.css('.price-display::text').extract_first()
        deal['price'] = clean_string(price)
        # it's dynamic
        # images = hxs.xpath('//div[@class="img-area"]//img/@src').extract()
        # deal['images'] = ','.join(images[:2])
        deal['category'] = response.request.meta['category']
        deal['partner'] = response.request.meta['partner']
        return deal
