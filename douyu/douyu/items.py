# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class douyuItem(Item):
    # define the fields for your item here like:
    url = Field()
    room_name = Field()
    people_count = Field()
    tag = Field()
