# -*- coding: utf-8 -*-
# @Time     : 2019/5/6 14:56
# @Author   : kevin
from scrapy import cmdline

name = 'maoyanmovie'
cmd = 'scrapy crawl {}'.format(name)
cmdline.execute(cmd.split())
