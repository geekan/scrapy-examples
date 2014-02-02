# Scrapy settings for sis project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sis'

SPIDER_MODULES = ['sis.spiders']
NEWSPIDER_MODULE = 'sis.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sis (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
    'sis.misc.middleware.CustomHttpProxyMiddleware': 400,
    'sis.misc.middleware.CustomUserAgentMiddleware': 401,
}

ITEM_PIPELINES = {
    'sis.pipelines.JsonWithEncodingPipeline': 300,
}

LOG_LEVEL = 'INFO'

