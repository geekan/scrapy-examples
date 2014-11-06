# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ZhihuPeopleItem(Item):
    # define the fields for your item here like:
    name = Field()
    sign = Field()
    location = Field()
    employment = Field()
    position = Field()
    education = Field()
    description = Field()
    agree = Field()
    thanks = Field()
    asks = Field()
    answers = Field()
    posts = Field()
    collections = Field()
    logs = Field()
    followees = Field()
    followers = Field()
    follow_topics = Field()

