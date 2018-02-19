# ecoding=utf-8
from scrapy import Spider, Selector, Request
from main_page.ZhiLianScrapy.items import ZhilianscrapyItem
from scrapy_redis.spiders import RedisSpider
import re,json,urllib
import traceback
import redis,time
class ZhiLianSpider(RedisSpider):
    name = "zhi_lian"
    allowed_domains = ['http://sou.zhaopin.com','http://jobs.zhaopin.com']
    redis_key = 'myspider:main_urls'
    no_repeat_urls=set()
    handle_httpstatus_list = [404,302]
    def __init__(self):
        self.rds = redis.StrictRedis(host='39.108.122.83', port='6379', decode_responses=True)
        self.page_size = 40
    def parse(self, response):
        request = response.request
        # html_doc = EncodingUtils.getStrNotKnowEcoding(response.body)
        # print(html_doc)
        link=urllib.request.unquote(request.url)
        print('解析网页。。。。'+link)
        select = Selector(response)
        lines=select.xpath('//*[@id="newlist_list_content_table"]/table')
        # 记录抓取次数（页数）
        page = int(link.split('p=')[1])
        if page <= self.page_size and len(lines) > 0:
            for job_url_obj in lines:
                job_url= job_url_obj.xpath('./tr[1]/td[1]/div/a/@href').extract_first()
                print('遍历职位链接>>>>>>>>>>>>>url:'+str(job_url))
                try:
                    if job_url:
                        if str(job_url) in self.no_repeat_urls:
                            print('重复链接。。。。。'+str(job_url))
                        else:
                            #---------->>>>>>>>>存ｒｅｄｉｓ
                            self.rds.lpush('myspider:details_urls',str(job_url))
                            #---------->>>>>>>>>存mysql
                            item=ZhilianscrapyItem()
                            # 获取关键字,地点
                            regex1 = re.compile('&kw=(.*?)&', re.S)
                            regex2 = re.compile('jl=(.*?)&', re.S)
                            kwd = regex1.findall(link, 0)
                            places = regex2.findall(link, 0)
                            if len(places) > 0:
                                item['place']= places[0]
                            else:
                                item['place'] = ''
                            if len(kwd) > 0:
                                item['keywords'] =kwd[0]
                            else:
                                item['keywords'] = ''
                            item['details_url'] = str(job_url)
                            yield item;
                    else:
                        print('职位链接不合法...'+str(job_url))
                        continue
                except Exception as e:
                    print('遍历职位链接，发生异常。。。。'+str(job_url))
                    traceback.print_exc()
                    continue
        if (response.status in self.handle_httpstatus_list)or (page<=self.page_size and len(lines) == 0):
            print("--------网页为空或４０４，３０２（实际状态：%d）---重新获取第 %d 页----------------%s" %(response.status,self.page,response.request.url))
            time.sleep(1)
            # request.meta["change_proxy"] = True
            yield request
        elif page<=self.page_size :
            page= page + 1
            time.sleep(1)
            preUrl = link.split('p=')[0]
            nextUrl = preUrl +'p='+ str(page)
            print("-----------获取第 %d 页----------------%s" % (page,nextUrl))
            yield Request(nextUrl, callback=self.parse, dont_filter=True)
