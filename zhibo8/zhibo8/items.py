# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SportItem(scrapy.Item):
    # define the fields for your item here like:
    #title = scrapy.Field()
    #url = scrapy.Field() 
    start_time = scrapy.Field() 
    home_team = scrapy.Field() 
    guest_team = scrapy.Field() 
    guest_team = scrapy.Field() 
    match_date = scrapy.Filed()
    game_type = scrapy.Filed()
    home_logo = scrapy.Filed()
    guest_logo = scrapy.Filed()
