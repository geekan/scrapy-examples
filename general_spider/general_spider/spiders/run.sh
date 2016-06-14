conf=${1:-scrapy_examples}
scrapy crawl general_spider -a conf_module=$conf
