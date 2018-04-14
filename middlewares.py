# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

from scrapy.exceptions import NotConfigured

from .settings import USER_AGENTS

# 随机选取 浏览器头信息
class RandomUserAgent(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', user_agent)


# 随机端口 重写scrapy方法
class RandomProxies(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        PROXIES=[]
        with open('../../myip.txt','w') as f:
            ip = f.readlines()
            PROXIES.append(ip)
        self.proxies = settings.getlist('PROXIES')
        self.stats = {}.fromkeys(self.proxies, 0)
        self.max_failed = 1

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)
        print('use %s as proxy' % request.meta['proxy'])

    def remove_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            print('proxy %s removed from proxies list' % proxy)

    def process_response(self, request, response, spider):
        cur_proxy = request.meta['proxy']
        if response.status >= 400:
            self.stats[cur_proxy] += 1
        if self.stats[cur_proxy] >= self.max_failed:
            self.remove_proxy(cur_proxy)
        return response

    def process_exception(self, request, exception, spider):
        print('raise exception:%s when use %s.' % (exception, request.meta['proxy']))
        self.remove_proxy(request.meta['proxy'])