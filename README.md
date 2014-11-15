scrapy-examples
==============

Multifarious scrapy examples with integrated proxies and agents, which make you comfy to write a spider.

Don't use it to do anything illegal!

####PREREQUISITE

* Scrapy
  > Check https://github.com/scrapy/scrapy

* Goagent
  > If you don't want to use proxy, just comment the proxy middleware in settings.  
  > Or if you want to custom it, you can hack `misc/proxy.py`.  
  > Its serviceability is decreasing fast, we should switch to another distributed proxy.  
  > Or the crawler would be ban easily.

***

##doubanbook spider

####Tutorial

    git clone https://github.com/geekan/scrapy-examples
    cd scrapy-examples/doubanbook
    scrapy crawl doubanbook

####Depth

There are several depths in the spider, and the spider gets
real data from depth2.

- Depth0: The entrance is `http://book.douban.com/tag/`
- Depth1: Urls like `http://book.douban.com/tag/外国文学` from depth0
- Depth2: Urls like `http://book.douban.com/subject/1770782/` from depth1

####Example image
![douban book](https://raw.githubusercontent.com/geekan/scrapy-examples/master/doubanbook/sample.jpg)

***

##Avaiable Spiders

* linkedin
  * linkedin
* tutorial
  * dmoz_item
  * douban_book
  * page_recorder
  * douban_tag_book
* doubanbook
  * doubanbook
* hrtencent
  * hrtencent
* sis
  * sis
* zhihu
  * zhihu
* alexa
  * alexa
  * alexa.cn
