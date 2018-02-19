#!  /usr/bin/env python
#ecoding=utf-8
from scrapy import cmdline

#scrapy crawl spider1 -L WARNING       这样爬虫断掉后，再启动会接着上次的 url 跑。
cmdline.execute("scrapy crawl zhi_lian".split())#:::spider name