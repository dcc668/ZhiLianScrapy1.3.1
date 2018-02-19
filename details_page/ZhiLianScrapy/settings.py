# -*- coding: utf-8 -*-
BOT_NAME = 'ZhiLianScrapy'

SPIDER_MODULES = ['ZhiLianScrapy.spiders']
NEWSPIDER_MODULE = 'ZhiLianScrapy.spiders'

ITEM_PIPELINES = {
    'ZhiLianScrapy.mysql_pipelines.MySQLPipeline': 600
}

IMAGES_STORE='.\Image'
#################    REDIS    获取url，获取ip的在代码中配置 #############################
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

REDIS_URL = None # 一般情况可以省去
REDIS_HOST = '39.108.122.83' # 也可以根据情况改成 localhost
REDIS_PORT = 6379
####################    MYSQL      #############################
# MYSQL_HOST = 'localhost'
# MYSQL_DBNAME = 'mydb'
# MYSQL_USER = 'root'
# MYSQL_PASSWD = '1234'
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'mydb'
MYSQL_USER = 'cc'
MYSQL_PASSWD = '1234'



LOG_LEVEL = 'DEBUG'
# DEPTH_LIMIT=1
# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

AUTOTHROTTLE_ENABLED = False


DOWNLOADER_MIDDLEWARES = {
   'ZhiLianScrapy.middlewares.ZhilianScrapySpiderMiddleware': 543,
    #代理ip
    # 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    # 'ZhiLianScrapy.middlewares.ProxyMiddleware':125,
    #使用ｔｏｍｊｓ，取消默认的useragent,使用新的useragent
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,  # 关闭默认下载器
    'ZhiLianScrapy.middlewares.JavaScriptMiddleware': 122,
    # 使用user agent池
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'ZhiLianScrapy.middlewares.MyUserAgentMiddleware': 124,

}
#代理报错：ip(failed 3 times): TCP connection timed out: 1006
RETRY_TIMES = 10
DOWNLOAD_TIMEOUT = 10 # 10-15 second is an experienmental reasonable timeout

#httperror_allowed_codes发生异常时也走parse方法，好在parse方法中处理异常页面
HTTPERROR_ALLOWED_CODES = [403,404,302,301]

#问题：代理ip请求次数太多酒重定向到验证码页面，关掉重定向,不会重定向到新的地址
REDIRECT_ENABLED = False

COOKIE = 'JSSearchModel=0; LastCity%5Fid=538; LastCity=%e4%b8%8a%e6%b5%b7; LastJobTag=%e4%ba%94%e9%99%a9%e4%b8%80%e9%87%91%7c%e8%8a%82%e6%97%a5%e7%a6%8f%e5%88%a9%7c%e7%bb%a9%e6%95%88%e5%a5%96%e9%87%91%7c%e5%91%98%e5%b7%a5%e6%97%85%e6%b8%b8%7c%e5%b8%a6%e8%96%aa%e5%b9%b4%e5%81%87%7c%e5%b9%b4%e5%ba%95%e5%8f%8c%e8%96%aa%7c%e5%ae%9a%e6%9c%9f%e4%bd%93%e6%a3%80%7c%e5%bc%b9%e6%80%a7%e5%b7%a5%e4%bd%9c%7c%e5%85%a8%e5%8b%a4%e5%a5%96%7c%e9%a4%90%e8%a1%a5%7c%e8%a1%a5%e5%85%85%e5%8c%bb%e7%96%97%e4%bf%9d%e9%99%a9%7c%e4%ba%a4%e9%80%9a%e8%a1%a5%e5%8a%a9%7c%e5%8a%a0%e7%8f%ad%e8%a1%a5%e5%8a%a9%7c%e9%80%9a%e8%ae%af%e8%a1%a5%e8%b4%b4%7c%e5%b9%b4%e7%bb%88%e5%88%86%e7%ba%a2%7c%e9%ab%98%e6%b8%a9%e8%a1%a5%e8%b4%b4%7c%e6%88%bf%e8%a1%a5%7c%e8%82%a1%e7%a5%a8%e6%9c%9f%e6%9d%83%7c%e5%8c%85%e4%bd%8f%7c%e5%85%8d%e8%b4%b9%e7%8f%ad%e8%bd%a6%7c%e5%8c%85%e5%90%83%7c%e6%af%8f%e5%b9%b4%e5%a4%9a%e6%ac%a1%e8%b0%83%e8%96%aa%7c%e5%88%9b%e4%b8%9a%e5%85%ac%e5%8f%b8%7c%e4%b8%8d%e5%8a%a0%e7%8f%ad%7c14%e8%96%aa%7c%e5%81%a5%e8%ba%ab%e4%bf%b1%e4%b9%90%e9%83%a8%7c%e4%bd%8f%e6%88%bf%e8%a1%a5%e8%b4%b4%7c%e9%87%87%e6%9a%96%e8%a1%a5%e8%b4%b4%7c%e6%97%a0%e8%af%95%e7%94%a8%e6%9c%9f%7c%e5%85%8d%e6%81%af%e6%88%bf%e8%b4%b7; LastSearchHistory=%7b%22Id%22%3a%226ca38def-9a0c-4c70-b218-d8635cc2c7a7%22%2c%22Name%22%3a%22java%e5%bc%80%e5%8f%91%e5%b7%a5%e7%a8%8b%e5%b8%88+%2b+%e4%b8%8a%e6%b5%b7%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fjl%3d%25e4%25b8%258a%25e6%25b5%25b7%26kw%3djava%25e5%25bc%2580%25e5%258f%2591%25e5%25b7%25a5%25e7%25a8%258b%25e5%25b8%2588%26p%3d1%26isadv%3d0%22%2c%22SaveTime%22%3a%22%5c%2fDate(1514106660529%2b0800)%5c%2f%22%7d; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; dywea=95841923.30885751908764452.1514106405.1514106405.1514106405.1; dyweb=95841923.17.9.1514106546215; dywec=95841923; dywez=95841923.1514106405.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; _qzja=1.739564104.1514106407357.1514106407357.1514106407358.1514106503416.1514106719376.0.0.0.3.1; _qzjb=1.1514106407357.3.0.0.0; _qzjc=1; _qzjto=3.1.0; _jzqa=1.3699347631316831700.1514106409.1514106409.1514106409.1; _jzqb=1.8.10.1514106409.1; _jzqc=1; _jzqckmp=1; __utma=269921210.2071327210.1514106410.1514106410.1514106410.1; __utmb=269921210.17.9.1514106546224; __utmc=269921210; __utmz=269921210.1514106410.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; BLACKSTRIP=yes; lastchannelurl=https%3A//passport.zhaopin.com/account/login%3FbkUrl%3Dhttps%253A%252F%252Fsou.zhaopin.com%252Fjobs%252Fsearchresult.ashx%253Fjl%253D%2525E4%2525B8%25258A%2525E6%2525B5%2525B7%2526kw%253Djava%2525E5%2525BC%252580%2525E5%25258F%252591%2525E5%2525B7%2525A5%2525E7%2525A8%25258B%2525E5%2525B8%252588%2526p%253D1%2526isadv%253D0%2523; pcc=r=444062600&t=1; firstchannelurl=https%3A//passport.zhaopin.com/account/login%3FbkUrl%3Dhttps%253A%252F%252Fsou.zhaopin.com%252Fjobs%252Fsearchresult.ashx%253Fjl%253D%2525E4%2525B8%25258A%2525E6%2525B5%2525B7%2526kw%253Djava%2525E5%2525BC%252580%2525E5%25258F%252591%2525E5%2525B7%2525A5%2525E7%2525A8%25258B%2525E5%2525B8%252588%2526p%253D1%2526isadv%253D0%2523; qrcodekey=3a84afae954c4ec6bc1a0faec5ba1c5d; JsNewlogin=2043605627; JSloginnamecookie=17693433417; JSShowname=%e8%91%a3%e8%87%a3%e8%87%a3; at=6d424bb346e646d78689e7e2b62b19bb; Token=6d424bb346e646d78689e7e2b62b19bb; rt=a33ccd06c00d4594a55dfa0787caffe7; uiioit=3D753D6A44640F38536D5F62043554684479527953390D6B566E203671645575496A42649; usermob=; userphoto=; userwork=0; bindmob=0; monitorlogin=Y; __xsptplusUT_30=1; dywem=95841923.y; __xsptplus30=30.1.1514106558.1514106673.2%234%7C%7C%7C%7C%7C%23%23l9HBdtfMrjU7zXIw4WPIt07m4TTk8bRM%23; JSpUserInfo=386B2E695671416557700469476D5B6A586B4977526F45355275216B246956714665587003694C6D586A5D6B4277566F443558755A6B51693E713965527056ED96EC88EB526B3477286F4D3558755C6B52695C7147655A700669436D526A5F6B3177146F013547750E6B056906714C653C706169486D5A6A526B3077316F4D3558755F6B4769597143654F700469426D516A586B41775E6F31352575506B5B69507122652E7008693F6D266A516B4077576F40355875556B5D695E71466554706069216D566A586B4A77366F393554755C6B51693E71276521700869446D5C6A5F6B4877566F44355A755E6B5E695A71406554709; SubscibeCaptcha=4FE323727A31774EFA24B6D377496B7F; loginreleased=1'
AGENTS = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)""," 
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"]
AGENTS2 = [
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
]
