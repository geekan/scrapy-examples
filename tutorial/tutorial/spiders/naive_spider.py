'''
This is a naive spider only for example
'''
from scrapy.spider import BaseSpider as Spider


class NaiveSpider(Spider):
    '''
    Download resources from start_urls.
    '''
    name = 'naive'
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
