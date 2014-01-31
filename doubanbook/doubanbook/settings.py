# Scrapy settings for doubanbook project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'doubanbook'

SPIDER_MODULES = ['doubanbook.spiders']
NEWSPIDER_MODULE = 'doubanbook.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubanbook (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
    'doubanbook.misc.middleware.CustomHttpProxyMiddleware': 400,
    'doubanbook.misc.middleware.CustomUserAgentMiddleware': 401,
}

LOG_LEVEL = 'INFO'

