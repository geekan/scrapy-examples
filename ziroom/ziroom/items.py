# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    room_id = scrapy.Field()
    room_price = scrapy.Field()
    room_name = scrapy.Field()
    modifyDate = scrapy.Field()
