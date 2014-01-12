# Scrapy settings for linkedin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os

BOT_NAME = 'linkedin'

SPIDER_MODULES = ['linkedin.spiders']
NEWSPIDER_MODULE = 'linkedin.spiders'

DOWNLOADER_MIDDLEWARES = {
    'linkedin.middleware.CustomHttpProxyMiddleware': 543,
    'linkedin.middleware.CustomUserAgentMiddleware': 545,
}

########### Item pipeline
ITEM_PIPELINES = [
                  "linkedin.pipelines.MongoDBPipeline",
]

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy'
MONGODB_COLLECTION = 'person_profiles'
MONGODB_UNIQ_KEY = '_id'
###########

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin (+http://www.yourdomain.com)'

# Enable auto throttle
AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False

# Set your own download folder
DOWNLOAD_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "download_file")


