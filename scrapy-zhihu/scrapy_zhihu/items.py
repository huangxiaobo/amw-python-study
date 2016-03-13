# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuTopicItem(scrapy.Item):
	title = scrapy.Field()
	desc = scrapy.Field()
	img = scrapy.Field()
	href = scrapy.Field()