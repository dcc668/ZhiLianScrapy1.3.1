# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhilianscrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = Field()  # 公司名称
    company_link = Field()  # 公司链接
    company_content = Field()  # 公司的介绍
    company_size = Field()#公司规模
    company_home_link = Field()#公司主页
    company_nature = Field()#公司性质
    company_industry = Field()#公司行业
    company_place = Field()#公司地址
    advantage = Field()  # 公司福利
    salary = Field()  # 职位月薪
    place = Field()  # 工作地点
    job_name = Field()  # 职位名称
    job_place = Field()  # 工作地点（具体）
    job_nature = Field()  # 工作性质
    job_number = Field()  # 招聘人数
    job_kind = Field()  # 职位类别
    job_content = Field()  # 职位描述
    post_time = Field()  # 发布日期
    work_experience = Field()  # 工作经验
    education = Field()  # 最低学历
    keywords = Field()  #关键词
