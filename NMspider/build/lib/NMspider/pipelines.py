# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os
import json
import socket
import pymongo
from datetime import datetime
from NMspider.settings import *

class NmspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongodbPiplines(object):
    def open_spider(self,spider):
        host = MONGO_CONF['MONGODB_HOST']
        port = MONGO_CONF['MONGODB_PORT']
        dbName = MONGO_CONF['MONGODB_DBNAME']
        self.client = pymongo.MongoClient(host=host, port=port)
        tdb = self.client[dbName]
        post_name = spider.name+'_data'
        self.post = tdb[post_name]

    def process_item(self, item, spider):

        data = dict(item)
        data['source'] = spider.name
        data['crawl_date'] = str(datetime.now().date())
        self.post.insert(data)
        return item
