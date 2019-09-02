# -*- coding: utf-8 -*-
import scrapy


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    # allowed_domains = ['m.sina.com']
    # start_urls = ['http://m.sina.com/']
    hot_url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot"

    def parse(self, response):
        pass
