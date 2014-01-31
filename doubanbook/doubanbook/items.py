# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DoubanbookItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()
    desc = Field()
    num = Field()


class DoubanSubjectItem(Item):
    title = Field()
    link = Field()
    info = Field()
    rate = Field()
    votes = Field()
    content_intro = Field()
    author_intro = Field()
    tags = Field()
