# Scrapy settings for v2ex project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
from os.path import dirname
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)
from misc.log import *

BOT_NAME = 'v2ex'

SPIDER_MODULES = ['v2ex.spiders']
NEWSPIDER_MODULE = 'v2ex.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'v2ex (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
   # 'misc.middleware.CustomHttpProxyMiddleware': 400,
    'misc.middleware.CustomUserAgentMiddleware': 401,
}

ITEM_PIPELINES = {
    'v2ex.pipelines.JsonWithEncodingPipeline': 300,
    #'v2ex.pipelines.RedisPipeline': 301,
}

LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 1
