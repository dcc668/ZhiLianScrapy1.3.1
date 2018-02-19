# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #UserAegent中间件
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from scrapy.conf import settings
import  random
import  pymongo
import datetime

class ZhilianScrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 使用user agent池
class MyUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        print('UserAgentMiddleware---------->>>使用user agent池')
        # cookie模拟登陆
        # request.headers["cookie"] = settings['COOKIE']
        request.headers["user-agent"] = random.choice(settings['AGENTS'])

import redis
class ProxyMiddleware():
    def __init__(self, ip=''):
        self.ip = ip
        r = redis.StrictRedis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], decode_responses=True)
        ips_str=r.get('ips')
        self.ips=ips_str.split('||')
        while '' in self.ips:
            self.ips.remove('')
        print('Redis服务器上获取代理ip ------------->>>>：' + str(self.ips))
    def process_request(self, request, spider):
        proxy_ip = random.choice(self.ips)
        print("ProxyMiddleware---------->>>proxy_ip:" + proxy_ip)
        request.meta["proxy"] = "http://" + proxy_ip
        request.headers["cookie"] = settings['COOKIE']

#（1）创建 下载中间件JavaScriptMiddleware
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import PhantomJS
from scrapy.http import HtmlResponse
from details_page.ZhiLianScrapy.settings import AGENTS2
import time
class JavaScriptMiddleware():
    def __init__(self):
        self.driver_init()
        self.is_reopen=False;
    def driver_init(self):
        tomJsDriver = r'../driver/phantomjs.exe';
        # 引入配置对象DesiredCapabilities
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        agent = random.choice(AGENTS2);
        dcap["phantomjs.page.settings.userAgent"] = agent
        dcap["phantomjs.page.customHeaders.User-Agent"] = agent
        # 不载入图片，爬页面速度会快很多
        dcap["phantomjs.page.settings.loadImages"] = False
        #是否启用js
        dcap["phantomjs.page.settings.javascriptEnabled"] = False
        dcap["phantomjs.page.settings.browserName"] = 'Chrome'
        # #打开带配置信息的phantomJS浏览器
        tomJs = PhantomJS(tomJsDriver, desired_capabilities=dcap)
        # 隐式等待5秒，可以自己调节
        tomJs.implicitly_wait(1)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        tomJs.set_page_load_timeout(10)
        # 设置10秒脚本超时时间
        tomJs.set_script_timeout(10)
        self.driver=tomJs
        self.add_cookies()
    #添加ｃｏｏｋｉｅｓ
    def add_cookies(self):
        cookies=settings['COOKIE'].split(';')
        for coo in cookies:
            key,value=coo.strip().split('=',1)
            cookie={}
            cookie['name']=key
            cookie['value'] = value
            self.driver.add_cookie({
                'domain': '.sou.zhaopin.com',  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })
    def process_request(self, request, spider):
        #每６分钟，重起ｔｏｍｊｓ
        now_time=int(time.strftime('%M', time.localtime()))
        if now_time%6==0:   #在6分钟内
            if self.is_reopen==False:
                print('--------------------------每６分钟，重起ｔｏｍｊｓ------------重新打开tomjs〉〉〉〉〉〉〉〉〉〉〉〉〉〉-----------------------------------------------------------------------')
                self.close_driver()
                self.driver_init()
                self.is_reopen =True
        elif  self.is_reopen==True and now_time%6!=0:  #出了6分钟
            self.is_reopen =False
        # js = "var q=document.documentElement.scrollTop=10000"
        # self.driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        self.driver.get(request.url)
        content = self.driver.page_source.encode('utf-8')
        # print('tomjs>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>请求结果：'+str(content,'utf-8'))
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    def __del__(self):
        self.close_driver()

    def close_driver(self):
        self.driver.quit()

