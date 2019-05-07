# -*- coding: utf-8 -*-

# Scrapy settings for maoyan project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# Scrapy项目的名字,这将用来构造默认 User-Agent,同时也用来log,当您使用 startproject 命令创建项目时其也被自动赋值。
BOT_NAME = 'maoyan'

# Scrapy搜索spider的模块列表 默认: [xxx.spiders]
SPIDER_MODULES = ['maoyan.spiders']

# 使用 genspider 命令创建新spider的模块。默认: 'xxx.spiders'
NEWSPIDER_MODULE = 'maoyan.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 爬取的默认User-Agent，除非被覆盖
# USER_AGENT = 'maoyan (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 如果启用,Scrapy将会采用 robots.txt策略  所以设置为False
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# Scrapy downloader 并发请求(concurrent requests)的最大值,默认: 16  如果不修改 则默认开启16个线程
CONCURRENT_REQUESTS = 6

# Configure a delay for requests for the same website (default: 0)
# 为同一网站的请求配置延迟（默认值：0）

# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# 下载器在下载同一个网站下一个页面前需要等待的时间,该选项可以用来限制爬取速度,减轻服务器压力。同时也支持小数:0.25 以秒为单位
DOWNLOAD_DELAY = 3  # 设置延迟现在时间

# The download delay setting will honor only one of:
# 下载延迟设置只有一个有效
# 对单个网站进行并发请求的最大值。
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值。如果非0,则忽略 CONCURRENT_REQUESTS_PER_DOMAIN
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 禁用Cookie（默认情况下启用） 所以一般需要打开为False
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# 禁用Telnet控制台（默认启用）
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'maoyan.middlewares.MaoyanSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'maoyan.middlewares.MaoyanDownloaderMiddleware': 543,
   # 'maoyan.middlewares.ProxyMiddleware': 543,
   'maoyan.middlewares.UAMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'maoyan.pipelines.MaoyanPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s|%(processName)s|%(threadName)s|%(levelname)s|%(filename)s:%(lineno)d|%(funcName)s|%(message)s'

# from datetime import datetime

# 文件及路径，log目录需要先建好
# today = datetime.now()
# LOG_FILE = "scrapy_{}_{}_{}.log".format(today.year, today.month, today.day)
