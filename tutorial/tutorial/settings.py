# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'
ITEM_PIPELINES = {
    #'tutorial.pipelines.JsonWithEncodingPipeline': 300,
}
#Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
    #'tutorial.misc.middleware.CustomHttpProxyMiddleware': 400,
    'tutorial.misc.middleware.CustomUserAgentMiddleware': 401,
}

LOG_LEVEL = 'INFO'
