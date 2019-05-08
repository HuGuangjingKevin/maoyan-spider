# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
class MaoyanPipeline(object):
    def __init__(self):
        Client = pymongo.MongoClient(
            host="127.0.0.1",
            port=27017,
        )
        self.MongoDB = Client["spider"]
        self.collection = self.MongoDB["maoyan"]

    def process_item(self, item, spider):
        logging.info(item)
        try:
            self.collection.insert(item)
        except Exception as e:
            pass
        return item
