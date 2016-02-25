#!/usr/bin/python
#-*- encoding=utf-8 -*-

import scrapy

class SpiderZhihu(scrapy.Spider):
	name = 'zhihu'

	allowed_domains = ['zhihu.org']
	start_urls = ''

	def parse(self, response):
		pass
