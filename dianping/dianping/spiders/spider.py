from scrapy.http import Request
from scrapy.selector import Selector

try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

from misc.spider import CommonSpider


class dianpingSpider(CommonSpider):
    name = "dianping"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://www.dianping.com/search/category/2/30/g141r1471",
    ]

    def parse(self, response):
        hxs = Selector(response)
        sites = hxs.xpath('//div[@class="tit"]/a/@href').extract()
        for site in sites:
            if site.startswith('/shop/'):
                yield Request("http://www.dianping.com{}".format(site), callback=self.parse_shop)

    def parse_shop(self, response):
        pass

        # categories = hxs.xpath(
        #     '//div[@class="%s"]/following-sibling::ul/li[@class="item has-panel"]' % self.MEDIA_CLASSES[
        #         self.media_type])
        # for category in categories:
        #     name = category.xpath('a/text()').extract()[0].strip()
        #     if name in self.IGNORE_CATEGORIES[self.media_type]:
        #         continue
        #     source_url = category.xpath('a/@href').extract()[0].strip()
