# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request
import re
import time

from ziroom.items import ZiroomItem

class Parse():
    def __init__(self, response):
        self.response = response
        self.room_detail = response.xpath('//div[@class="room_detail_right"]')[0]
        self.room_info = ' '.join(self.room_detail.xpath('.//ul[@class="detail_room"]/li/text()').extract())
        self.metro_info = ''.join(self.room_detail.xpath('.//span[@id="lineList"]/text()').extract()).replace(' ', '').replace('\n',
                                                                                                                  '')
    def getID(self):
        return int(re.findall('\d+', self.response.url)[0])
    def getName(self):
        return self.room_detail.xpath('.//h2/text()').extract()[0].replace(' ', '').replace('\n', '')
    def getPrice(self):
        room_price = int(self.room_detail.xpath('.//span[@class="room_price"]/text()').extract()[0][1:])
        if room_price < 500:
            room_price *= 30
        return room_price



class PagesSpider(Spider):
    name = "ziroom"
    start_urls = ['http://www.ziroom.com/z/nl/z3.html?p=1']

    def parse(self, response):
        print response.url
        page = re.findall('p=(\d+)', response.url)[0]

        houseList = response.xpath('//ul[@id="houseList"]/li')
        for each in houseList:
            url = each.xpath('div/h3/a/@href').extract()[0][2:].encode('utf-8')
            yield Request('http://' + url, self.parseItem)

        url = response.url
        url_new = url.replace(page, str(int(page) + 1))
        # yield Request(url_new, self.parse)

    def parseItem(self, response):
        p = Parse(response)
        item = ZiroomItem()
        item['modifyDate'] = int(time.time())
        item['room_id'] = p.getID()
        item['room_price'] = p.getPrice()
        item['room_name'] = p.getName()
        yield item