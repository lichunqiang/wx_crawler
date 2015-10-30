# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import logging
from settings import DATAHOME as _DATA_DIR

class WeixinPipeline(object):
	"""
	Pipe the data to file
	"""
	def __init__(self):
		self.file = open(_DATA_DIR + 'article.j1', 'w')

	def process_item(self, item, spider):
		try:
			line = json.dumps(dict(item)) + "\n"
		except Exception, e:
			logging.error(e)
		self.file.write(line)
		return item

	def spider_closed(self, spider):
		self.file.close()
