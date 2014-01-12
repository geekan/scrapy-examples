scrapy-linkedin
===============

Using Scrapy to get Linkedin's person public profile.

### feature
* Get all **public** profile
* Using Scrapy
* Enable auto throttle
* Enable naive proxy providing
* Agent rotating
* Support Unicode
* Using MongoDB as Backend
* ...


### Dependency
* Scrapy == 0.20
* pymongo 
* BeautifulSoup4, UnicodeDammit


### usage
	1. start a MongoDB instance, `mongod`
	2. run the crawler, `scrapy crawl LinkedinSpider`

you may found `Rakefile` helpful.


### configuration
you can change MongoDB setting ang other things in `settings.py`. 

### note
if you just need whatever public profiles, there are better ways to do it. 
check out these urls: http://www.linkedin.com/directory/people/[a-z].html

Our strategy is following `also-view` links in public profile.

### One more thing
This is a toy project a few years ago. Now I won't maintain it anymore, questions about this project will be ignored. You can read the code, there isn't much. 
I hope this project can help you get a basic understanding of Scrapy, then you can make your own Spider. 
