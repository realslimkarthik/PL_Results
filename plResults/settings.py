# Scrapy settings for plResults project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'plResults'

SPIDER_MODULES = ['plResults.spiders']
NEWSPIDER_MODULE = 'plResults.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
CONCURRENT_REQUESTS = 1

# DEFAULT_REQUEST_HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Ubuntu Chromium/24.0.1312.56 Chrome/24.0.1312.56 Safari/537.17')
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
# }
#DOWNLOAD_DELAY = 2000

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'plResults (+http://www.yourdomain.com)'
