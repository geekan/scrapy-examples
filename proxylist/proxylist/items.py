# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class freeProxyListItem(Item):
    # define the fields for your item here like:
    ip = Field()
    port = Field()
    code = Field()
    country = Field()
    anonymity = Field()
    google = Field()
    https = Field()
    last_checked = Field()

