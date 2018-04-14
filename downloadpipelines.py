# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests


# 本地下载
class SinaPipeline(object):
    def process_item(self, item, spider):
        # 一级路径
        dir1 = os.getcwd() + '\\' + item['dir1']
        # 二级路径
        dir2 = dir1 + '\\' + item['dir2']
        # 三级路径---->>> 存放新闻 和 新闻相关照片
        dir3 = dir2 + '\\' + item['title'][:10].replace(':', '').replace('\\', '').replace('\/', '').replace('?', '')
        # 新闻详情文件名
        filename = dir3 + '\\' + item['title'][:10] + '.txt'
        # 如果不存在相关文夹件名 责创建
        if not os.path.isdir(dir1):
            os.makedirs(dir1)
        if not os.path.isdir(dir2):
            os.makedirs(dir2)
        if not os.path.isdir(dir3):
            os.makedirs(dir3)
        # 创建新闻详情文档
        with open(filename, 'wb') as f:
            f.write(item['content'].encode('utf-8'))
            f.flush()
        # 如果照片属性不为空
        if len(item['img']) != 0:
            # 取出列表里链接
            for link in item['img']:

                # 以列表下标 创建照片保存路径
                imgname = dir3 + '\\' + str(item['img'].index(link)) + link[-4:]

                # 创建并保存照片
                with open(imgname, 'wb') as f:
                    img = requests.get(link).content
                    print('=======================')
                    f.write(img)
                    f.flush()
        return item
