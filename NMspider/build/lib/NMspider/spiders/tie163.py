# -*- coding: utf-8 -*-
import json
import math
import urllib.parse
import scrapy
from NMspider.items import NmspiderItem

class Tie163Spider(scrapy.Spider):
    name = 'tie163'
    # allowed_domains = ['tie.163.com']
    # start_urls = ['http://tie.163.com/']
    index_url = "https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/recommendList/single?ibc=newspc&offset={offset}&limit=30"
    comment_url = "https://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{docId}/comments/newList?ibc=newspc&limit=30&offset={offset}"

    def start_requests(self):
        for i in range(3):
            yield scrapy.Request(url=self.index_url.format(offset=30*i),callback=self.parse)

    def parse(self, response):
        for nm in json.loads(response.text):
            thread = nm.get("thread",{})
            item = NmspiderItem()
            item['title'] = thread['title']
            item['url'] = thread['url']
            docId = thread['docId']
            print("=========\n%s\n%s\n%s\n========"%(thread['title'],thread['boardId'],thread['url']))
            yield scrapy.Request(url=thread['url'], callback=self.parse_context, meta={'item': item, 'docId': docId},
                                 dont_filter=True)

    def parse_context(self, response):
        item = response.meta['item']
        docId = response.meta['docId']
        url_local = urllib.parse.urlsplit(response.url).netloc

        if url_local == 'dy.163.com':
            item['context'] = ''.join(response.xpath('.//div[@id="content"]/p/text()').extract())
        else:
            item['context'] = ''.join(response.xpath('.//div[@id="endText"]/p/text()').extract())
        yield scrapy.Request(url=self.comment_url.format(docId=docId,offset=0), callback=self.parse_comment_scheduler,
                             meta={'item': item, 'docId': docId}, dont_filter=True)

    def parse_comment_scheduler(self,response):
        comment_json = json.loads(response.text)
        comment_limit = comment_json['newListSize']
        # print(comment_limit)
        page_num = math.ceil(comment_limit/30)
        docId = response.meta['docId']
        for i in range(1,page_num+1):
            item = response.meta['item']
            yield scrapy.Request(url = self.comment_url.format(docId=docId,offset = str(30*i)),callback = self.parse_comment,meta = {'item':item},dont_filter=True)

    def parse_comment(self,response):

        comment_json = json.loads(response.text)
        comments = comment_json['comments']
        for comment_item in comments.values():
            item = response.meta['item']
            item['comment'] = comment_item['content']
            item['comment_user'] = comment_item['user'].get('nickname','游客用户')
            item['support'] = comment_item['vote']
            item['user_location'] = comment_item['user'].get('location')
            yield item
