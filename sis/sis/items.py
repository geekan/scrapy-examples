# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SisItem(Item):
    title = Field()
    link = Field()
    imgs = Field()
    torrents = Field()
    sharetitle  = Field()
    bottomline = Field()
    duty = Field()
    xxx = Field()

class SisForumListItem(Item):
    content = Field() # raw content with all html
    title = Field()
    thread_type = Field()
    author = Field()
    post_time = Field()
    link = Field()
    star = Field()
    comment = Field()
    view = Field()
    size = Field()
    video_type = Field()
    last_post_time = Field()
