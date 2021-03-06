# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class ScrapyZhihuTopicPipeline(object):
	def __init__(self):
		self.file = codecs.open('zhihu_topics.json', 'w', 'utf-8')

	def process_item(self, item, spider):
		if type(item).__name__ not in ['ZhihuTopicItem', ]:
			return item
		line = json.dumps(dict(item), ensure_ascii = False) + '\r\n'
		self.file.write(line)

		return item

	def spider_closed(self, spider):
		self.file.close()

class ScrapyZhihuTopAnswerPipeline(object):
	def __init__(self):
		self.file = codecs.open('zhihu_top_answers.json', 'w', 'utf-8')

	def process_item(self, item, spider):
		if type(item).__name__ not in ['ZhihuTopAnswerItem', ]:
			return item		
		line = json.dumps(dict(item), ensure_ascii = False) + '\r\n'
		self.file.write(line)

		return item

	def spider_closed(self, spider):
		self.file.close()