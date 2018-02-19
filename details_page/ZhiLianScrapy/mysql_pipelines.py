# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql.cursors
import time
from sshtunnel import SSHTunnelForwarder

class MySQLPipeline(object):
        # Connect to the MySQL database
        def __init__(self):
            self.server= SSHTunnelForwarder(
                    ('39.108.122.83', 22),
                    ssh_password="Dcc1234&",
                    ssh_username="root",
                    remote_bind_address=('172.18.150.104', 3306))
            self.server.start()  # start ssh sever
            local_port = self.server.local_bind_port
            #连接配置信息
            config = {
                    'host': settings['MYSQL_HOST'],
                    'port': local_port,
                    'user': settings['MYSQL_USER'],
                    'password': settings['MYSQL_PASSWD'],
                    'db': settings['MYSQL_DBNAME'],
                    'charset': 'utf8',
                    'cursorclass': pymysql.cursors.DictCursor,
                }
            # 创建连接
            self.connection = pymysql.connect(**config)
            # 创建数据表zhilian
            self.create_table()

        # 创建数据表创建数据表zhilian_job_details_contents
        def create_table(self):
            cursor = self.connection.cursor()
            create_sql = "create table if not exists zhilian_job_details_contents(" \
                         "id int(11) not null auto_increment," \
                         "job_name varchar(255) default null," \
                         "company_name varchar(255) default null," \
                         "company_link varchar(255) default null," \
                         "advantage varchar(255) default null," \
                         "salary varchar(255) default null," \
                         "place varchar(255) default null," \
                         "post_time varchar(255) default null," \
                         "job_nature varchar(255) default null," \
                         "work_experience varchar(255) default null," \
                         "education varchar(255) default null," \
                         "job_number varchar(255) default null," \
                         "job_kind varchar(255) default null," \
                         "job_content TEXT," \
                         "job_place varchar(255) default null," \
                         "company_content TEXT," \
                         "company_size varchar(255) default null," \
                         "company_nature varchar(255) default null," \
                         "company_industry varchar(255) default null," \
                         "company_home_link varchar(255) default null," \
                         "company_place varchar(255) default null," \
                         "keywords varchar(255) default null," \
                         "scrapy_time varchar(255) default null," \
                         "primary key(id)) ENGINE=MyISAM DEFAULT CHARSET=utf8"
            cursor.execute(create_sql)
            self.connection.commit()
            cursor.close()
            print('数据表创建成功')
        def process_item(self, item, spider):
            # 将信息插入到数据库中
            cursor = self.connection.cursor()
            args = (
                item['company_name'],
                item['company_link'],
                item['company_content'],
                item['company_size'],
                item['company_home_link'],
                item['company_nature'],
                item['company_industry'],
                item['company_place'],
                item['advantage'],
                item['salary'],
                item['place'],
                item['job_name'],
                item['job_place'],
                item['job_nature'],
                item['job_number'],
                item['job_kind'],
                item['job_content'],
                item['post_time'],
                item['work_experience'],
                item['education'],
                item['keywords'],
                time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            )
            newsSqlText = "insert into zhilian_job_details_contents(company_name," \
                "company_link,company_content," \
                "company_size,company_home_link," \
                "company_nature,company_industry," \
                "company_place,advantage," \
                "salary,place," \
                "job_name,job_place," \
                "job_nature,job_number," \
                "job_kind,job_content," \
                "post_time,work_experience," \
                "education,keywords," \
                "scrapy_time)values(" \
                          "%s,%s,%s,%s,%s," \
                          "%s,%s,%s,%s,%s," \
                          "%s,%s,%s,%s,%s," \
                          "%s,%s,%s,%s,%s," \
                          "%s,%s)"
            print(newsSqlText)
            cursor.execute(newsSqlText,args)
            print('执行sql，完成！')
            self.connection.commit()
            cursor.close()
            return item

        def __del__(self):
            self.connection.close()
            self.server.stop()


