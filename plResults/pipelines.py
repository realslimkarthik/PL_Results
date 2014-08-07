# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
import items
from pymongo import MongoClient

class LinkPipeline(object):
    def __init__(self):
        self.client = MongoClient()

    def process_item(self, item, spider):
        if spider.name == 'PlL':
            db = self.client.plDB
            mLinks = db.matchLinks
            data = {}
            mLinks.insert(data)
        #return item