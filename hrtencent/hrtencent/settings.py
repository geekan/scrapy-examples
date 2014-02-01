# Scrapy settings for hrtencent project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hrtencent'

SPIDER_MODULES = ['hrtencent.spiders']
NEWSPIDER_MODULE = 'hrtencent.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hrtencent (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
    'hrtencent.misc.middleware.CustomHttpProxyMiddleware': 400,
    'hrtencent.misc.middleware.CustomUserAgentMiddleware': 401,
}

ITEM_PIPELINES = {
    'hrtencent.pipelines.JsonWithEncodingPipeline': 300,
}

LOG_LEVEL = 'INFO'

