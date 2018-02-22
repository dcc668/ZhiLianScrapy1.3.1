#!  /usr/bin/env python
#ecoding=utf-8
import redis
rds= redis.StrictRedis(host='39.108.122.83', port='6379', decode_responses=True)
place_name = ['北京', '上海', '广州', '深圳', '天津', '武汉', '西安', '成都', '大连', '长春', '沈阳', '南京', '济南', '青岛',
              '杭州', '苏州', '无锡', '宁波', '重庆', '郑州', '长沙', '福州', '厦门', '哈尔滨', '石家庄', '合肥', '惠州']
job_name = ['数据分析', 'php', '大数据', 'java', 'UI', 'IOS', '安卓', 'C++', 'python', '前端', '.net', '测试', '产品经理', '网络营销',
            '嵌入式', '项目经理', 'VR', 'AR','爬虫工程师','数字图像处理','机器学习']
print('+++++++++++++lpush start+++++++++++++++')
print('++++++place count：'+str(len(place_name)))
print('++++++job_name count：'+str(len(job_name)))
for place in place_name:
    print('++++++place：' + str(place))
    for keyword in job_name:
        url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + str(place) + '&kw=' + keyword+'&sm=0&isfilter=1&p=1'
        rds.lpush('myspider:main_urls', url)
# url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=上海&kw=php&sm=0&isfilter=1&p=1'
# url2 ="http://sou.zhaopin.com/jobs/searchresult.ashx?jl=上海&kw=大数据&sm=0&isfilter=1&p=1"
# # rds.lpush('myspider:main_urls',url)
print('+++++++++++++lpush finish+++++++++++++++')