# encoding:utf8
"""
虎扑新闻抓取
"""
import scrapy

class HupuNewsSpider(scrapy.Spider):
    name = "hupu_news"
    allowed_domains = ["hupu.com"]
    start_urls = ["http://voice.hupu.com/nba/newslist"]

    def parse(self, response):
        # refer : http://scrapy-chs.readthedocs.org/zh_CN/0.24/topics/selectors.html#topics-selectors-relative-xpaths
        li_list = response.xpath('//div[@class="news-list"]/ul/li')
        for li in li_list:
            #print li.extract()
            a = li.xpath('div/h4/a[1]')
            #print a.extract()
            title = li.xpath('div/h4/a[1]/text()').extract()
            link = li.xpath('div/h4/a[1]/@href').extract()
            print title[0],link[0]
