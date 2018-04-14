# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql.cursors import DictCursor


# 将数据保存到mysql
class SinaPipeline(object):

    # spider 自动调用函数 链接mysql数据库
    def open_spider(self, spider):
        self.con = pymysql.connect(

            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='zhang',
            charset='utf8'

        )
        self.cur = self.con.cursor(DictCursor)

    # 存入数据库, 因为数据问题会发生sql注入
    def process_item(self, item, spider):
        # args = (item['dir1'], item['dir2'], item['url'], item['title'], item['content'], item['img'])
        # sql = "insert into news WHERE content='%s'"
        # sql = "select dir1, dir2, url, title, content,img from news where dir1= '%s',dir2= '%s',url= '%s',title= '%s'," \
        #       "content= '%s',img= '%s'"
        # self.cur.execute(sql%(item['dir1'], item['dir2'], item['url'], item['title'].replace('\'\'\' (0x27)',''),
        # item['content'].replace('\'\'\' (0x27)',''),
        #                       item['img']))
        # self.cur.execute(sql,[item['content'].replace('\u3000','')])
        print('--------------------------------')
        # sql = "select dir1,dir2,url,title,content,img from news SET dir1= %s,dir2= %s,url= %s,title= %s," \
        #       "content= '%s',img= '%s'"


        # 防注入
        sql = " insert into news(dir1,dir2,url,title,content,img) VALUES (%s,%s,%s,%s,%s,%s)"
        self.cur.execute(sql, (item['dir1'], item['dir2'], item['url'], item['title'], item['content'], item['img']))

        self.con.commit()
        return item


    # 关闭数据库
    def close_spider(self, spider):
        self.cur.close()
        self.con.close()
