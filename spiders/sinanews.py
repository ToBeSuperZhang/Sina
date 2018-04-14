# -*- coding: utf-8 -*-
import scrapy
from ..items import SinaItem


class SinanewsSpider(scrapy.Spider):
    name = 'sinanews'
    allowed_domains = ['http://news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']
    item = SinaItem()

    # 获取 第一标题,第二标题,和子类链接
    def parse(self, response):
        fist_title_list = response.xpath("//*[@id='tab01']/div")
        # for i in range(3):
        ## 打开注释 责全检索爬取

        for i in range(len(fist_title_list)):
            dir1 = fist_title_list[i].xpath(".//h3/a/text()").extract_first()
            print(dir1)
            second_title_list = self.item['dir2'] = fist_title_list[i].xpath(".//li")
            for second_title in second_title_list[:3]:
                dir2 = second_title.xpath("./a/text()").extract_first()
                second_url = second_title.xpath("./a/@href").extract_first()

                # 因为异步, 为确保信息一一对应, 通过meta将数据传递给下级函数
                request = scrapy.Request(second_url, callback=self.parse_second_url, dont_filter=True)
                request.meta['first_title'] = dir1
                request.meta['second_title'] = dir2
                yield request

    # 获取子类链接,并解析 下一级链接
    def parse_second_url(self, response):
        second_url = response.xpath("//div[@class='links']/a[1]/@href").extract_first()
        if second_url:
            request = scrapy.Request(second_url, callback=self.parse_news_url, dont_filter=True)
            request.meta['first_title'] = response.meta['first_title']
            request.meta['second_title'] = response.meta['second_title']
            request.meta['page_num'] = 1
            yield request

    # 获取新闻内容链接,和所有同级链接
    def parse_news_url(self, response):
        news_url_list = response.xpath("//ul[@class='list_009']/li/a/@href|//span[@class='c_tit']/a/@href").extract()
        print(news_url_list)
        if news_url_list:
            for news_url in news_url_list:
                request = scrapy.Request(news_url, callback=self.parse_news_info, dont_filter=True)
                request.meta['first_title'] = response.meta['first_title']
                request.meta['second_title'] = response.meta['second_title']
                request.meta['url'] = news_url
                yield request
            # page_num = response.meta['page_num']
            ## 获取所有同级网页信息
            # for i in range(1):
            #     # while True:
            #     page_num += 1
            #     print(page_num)
            #     if response.url.endswith('.shtml'):
            #         news_page = 'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_' + str(page_num) + '.shtml'
            #     else:
            #         news_page = 'http://roll.news.sina.com.cn/s/channel.php?ch=01#col=91&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page=' + str(
            #             page_num)

            ## 将链接传回给本函数
            #     request = scrapy.Request(news_page, callback=self.parse_news_url)
            #     request.meta['page_num'] = page_num
            #     yield request


    # 解析新闻网页信息,并获取需要内容
    def parse_news_info(self, response):
        title = ''.join(response.xpath("//div[@class='article']//p[1]/text()|"
                                       "//div[@class='page-header']/h1/text()").extract(
                                        ))
        if not title:
            self.item['title'] = '页面错误'
        else:
            self.item['title'] = title
        content = '\n'.join(response.xpath("//div[@class='article']//p/text()|"
                                         "//div[@class='article article_16']//p/text()").extract(
                                        )[1:])
        if not content:
            self.item['content'] = '页面错误'
        else:
            self.item['content'] = content
        img_links = response.xpath("//div[@class='article']//img/@src|"
                                   "//div[@class='article article_16']//img/@src").extract()
        if img_links:
            self.item['img'] = ','.join(img_links)
        else:
            self.item['img'] = ''
        self.item['dir1'] = response.meta['first_title']
        self.item['dir2'] = response.meta['second_title']
        self.item['url'] = response.meta['url']

        # 将item 传递给pipelines 执行本地存储 或者 链接mysql数据库
        yield self.item
