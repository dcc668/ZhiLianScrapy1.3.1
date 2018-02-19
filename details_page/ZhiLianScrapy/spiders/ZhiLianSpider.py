# ecoding=utf-8
from scrapy import Spider, Selector, Request
from details_page.ZhiLianScrapy.items import ZhilianscrapyItem
from scrapy_redis.spiders import RedisSpider
import re,json,time
from details_page.ZhiLianScrapy.ecoding_utils import  EncodingUtils

class ZhiLianSpider(RedisSpider):
    name = "zhi_lian"
    allowed_domains = ['http://sou.zhaopin.com','http://jobs.zhaopin.com']
    redis_key = 'myspider:details_urls'
    handle_httpstatus_list = [404,403,302,301]
    def __init__(self):
        self.page = 1
    def parse(self, response):
        request = response.request
        print('解析网页。。。。'+request.url)
        link=request.url
        if response.status in self.handle_httpstatus_list:
            print("--------详细页面%d---重新获取...%s" %(response.status,link))
            time.sleep(1)
            request.meta["change_proxy"] = True
            yield request
        else:
            print('获取详细页面的信息。url->'+link)
            select = Selector(response)
            item=ZhilianscrapyItem()
            item['keywords']=''
            for i in select.xpath('//div[@class="fixed-inner-box"]/div[1]'):
                job_name = i.xpath('h1/text()').extract_first()  # 职位名称
                company_name = i.xpath('h2/a/text()').extract_first() # 公司名称
                company_link = i.xpath('h2/a/@href').extract_first()  # 公司链接
                advantage = i.xpath('div[1]/span/text()').extract_first() # 公司福利
                item['job_name']=str(job_name) if job_name else ''
                item['company_name'] =str(company_name)if company_name else ''
                item['company_link'] =str(company_link)if company_link else ''
                item['advantage'] =str(advantage)if advantage else ''
            for i in select.xpath('//ul[@class="terminal-ul clearfix"]'):
                salary = i.xpath('li[1]/strong/text()').extract_first()  # 职位月薪
                place = i.xpath('li[2]/strong/a/text()').extract_first()  # 工作地点
                post_time = i.xpath('li[3]//span[@id="span4freshdate"]/text()').extract_first()  # 发布日期
                job_nature = i.xpath('li[4]/strong/text()').extract_first()  # 工作性质
                work_experience = i.xpath('li[5]/strong/text()').extract_first()  # 工作经验
                education = i.xpath('li[6]/strong/text()').extract_first()  # 最低学历
                job_number = i.xpath('li[7]/strong/text()').extract_first()  # 招聘人数
                job_kind = i.xpath('li[8]/strong/a/text()').extract_first()  # 职位类别
                item['salary']=str(salary)if str(salary) else ''
                item['post_time'] =str(post_time)if post_time else ''
                item['job_nature'] =str(job_nature)if job_nature else ''
                item['work_experience'] =str(work_experience)if work_experience else ''
                item['education'] =str(education)if education else ''
                item['job_number'] =str(job_number)if job_number else ''
                item['job_kind'] =str(job_kind)if job_kind else ''
                item['place'] = str(place) if place else ''
            reg = r'<!-- SWSStringCutStart -->(.*?)<!-- SWSStringCutEnd -->'
            reg = re.compile(reg, re.S)
            html_doc = EncodingUtils.getStrNotKnowEcoding(response.body)
            content = re.findall(reg,html_doc)
            try:
                content = content[0].strip()  # strip去空白
                reg_1 = re.compile(r'<[^>]+>')  # 去除html标签
                content = reg_1.sub('', content).replace('&nbsp', '')
                job_content = content  # 职位描述
            except Exception as e:
                job_content = ''
            item['job_content'] = str(job_content)if job_content else ''
            for i in select.xpath('//div[@class="tab-inner-cont"]')[0:1]:
                job_place = str(i.xpath('h2/text()').extract_first()).strip()  # 工作地点（具体）
                item['job_place'] = str(job_place)if job_place else ''
            for i in select.xpath('//div[@class="tab-inner-cont"]')[1:2]:
                company_content = str(i.xpath('string(.)').extract_first())\
                    .strip()\
                    .replace('\r\n', '。')\
                    .replace('\xa0', '')\
                    .replace(' ', '')# 公司的介绍
                item['company_content'] = company_content if company_content else ''
            for i in select.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]'):
                if len(i.xpath('li'))>=5:
                    company_size = i.xpath('li[1]/strong/text()').extract_first()
                    company_nature = i.xpath('li[2]/strong/text()').extract_first()
                    company_industry = i.xpath('li[3]/strong/a/text()').extract_first()
                    company_home_link = i.xpath('li[4]/strong/a/text()').extract_first()
                    company_place = i.xpath('li[5]/strong/text()').extract_first()
                else:
                    company_size = i.xpath('li[1]/strong/text()').extract_first()
                    company_nature = i.xpath('li[2]/strong/text()').extract_first()
                    company_industry = i.xpath('li[3]/strong/a/text()').extract_first()
                    company_home_link = [u'无公司主页']
                    company_place = i.xpath('li[4]/strong/text()').extract_first()
                item['company_size']= str(company_size)if company_size else ''
                item['company_nature']= str(company_nature)if company_nature else ''
                item['company_industry']= str(company_industry)if company_industry else ''
                item['company_home_link']= str(company_home_link)if company_home_link else ''
                item['company_place']= str(company_place).strip()if company_place  else ''
            json_str = json.dumps(item, default=lambda o: o.__dict__, sort_keys=True)
            print('详细页'+link+'处理结果：'+json_str)
            if item['job_content']=='' or item['job_content']==None:
                print("--------详细页面%d---内容没获取到。。。...%s" % (response.status, link))
                if 'http://xiaoyuan.zhaopin.com' in link:
                    print('http://xiaoyuan.zhaopin.com 链接不处理。。。。。');
                else:
                    pass;
                    # html_doc = EncodingUtils.getStrNotKnowEcoding(response.body)
                    # print(html_doc)
                    # time.sleep(1)
                    # item_list=self.get_content2(response)#有可能是手机的user_agent
                    # print('2次获取详细页结果：' + str(item_list))
                    # if len(item_list) == 1 and item_list[0] == '':
                    # request = Request((str(link)), callback=self.parse, dont_filter=True)
                    # request.meta["change_proxy"] = True
                    # yield request
            else:
                print('持久化到MySQL。。。。')
                yield item;

    #设备为手机时
    def get_content2(self, response):#有可能是手机的user_agent
        select = Selector(response)
        '''2次获取详细页面的信息'''
        item_list2 = []
        for i in select.xpath('//div[@class="about-position"]'):
            job_name = i.xpath('div[1]/h1/text()').extract_first()  # 职位名称
            salary=i.xpath('div[1]/div[1]/text()').extract_first()
            clearfix=i.xpath('div[1]/div[2]/text()').extract_first()
            company_name = i.xpath('div[2]/text()').extract_first()  # 公司名称
            address = i.xpath('div[3]/div[1]/span[1]/text()').extract_first()
            jingyan = i.xpath('div[3]/div[1]/span[2]/text()').extract_first()
            xueli= i.xpath('div[3]/div[1]/span[3]/text()').extract_first()
            time_fr=i.xpath('div[3]/div[2]/text()').extract_first()
            item_list2.append([str(job_name), str(salary), str(company_name), str(clearfix), str(company_name),address,jingyan,xueli,time_fr])
        for i in select.xpath('//div[@class="companyAdd boxsizing"]'):
            work_address = i.xpath('div[1]/text()').extract_first()#工作地址
            item_list2.append([str(work_address)])
        for i in select.xpath('//div[@class="tag-list"]'):
            strss=''
            for span in  i.xpath('span'):# 职位特点
                strss=strss+str(span.xpath('text()').extract_first())+','
            item_list2.append([str(strss)])
        for i in select.xpath('//article[@class="company-info"]'):#company-info
            type1 = i.xpath('a/div[2]/p[1]/text()').extract_first()  #互联网/电子商务
            type2 = i.xpath('a/div[2]/p[2]/text()').extract_first()  #民营
            item_list2.append([str(type1),str(type2)])
        return item_list2