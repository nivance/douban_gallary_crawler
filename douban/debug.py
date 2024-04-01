# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import os
import sys

# 添加当前项目的绝对地址
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 执行Scrapy的execute函数，使用crawl命令进行调试
execute(['scrapy', 'crawl', 'gallary'])