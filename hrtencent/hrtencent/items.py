# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PositionDetailItem(Item):
    title = Field()
    link = Field()
    sharetitle  = Field()
    bottomline = Field()
    duty = Field()
    xxx = Field()
