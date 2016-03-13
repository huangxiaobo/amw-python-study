#!/usr/bin/python
# -*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy_zhihu.items import ZhihuTopicItem
import scrapy
import json

class SpiderZhihu(CrawlSpider):
	name = 'zhihu'

	allowed_domains = ['www.zhihu.com']

	start_urls = [
		'https://www.zhihu.com/topics'
		]

	headers = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-US,en;q=0.8,zh;q=0.6",
		"Connection": "keep-alive",
		"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36",
		"Referer": "https://www.zhihu.com/"
		}

	cookie = {
		"q_c1" : "b56bd59fe73d4455a69868c0af9b3657|1456057507000|1456057507000",
		"_za" : "92042ac0-9d25-4101-86fc-600546441405",
		"_xsrf" : "464d07628dc5d61f9dfb9b4ae5d33838",
		"__utmt" : "1",
		"cap_id" :"Mzk2ZTE5YjU0MTBjNDZiMDkyYTFjOTdlNjNhMzhkOWM=|1456408025|95ad7e0fb87573b8f02933d0685c9ebccf1e9481",
		"__utma" : "51854390.1513330630.1456407439.1456407439.1456407439.1",
		"__utmb" : "51854390.10.10.1456407439",
		"__utmc" : "51854390",
		"__utmz" : "51854390.1456407439.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/login",
		"__utmv" : "51854390.000--|2=registration_date=20130817=1^3=entry_date=20160221=1",
		"n_c" : "1"
		}

	def __init__(self):
		super(CrawlSpider, self).__init__()
		self.topic_offset = 0

	def start_requests(self):
		"""start_requests."""
		return [scrapy.FormRequest(
			"https://www.zhihu.com/login/email",
			formdata = {"email" : "767806886@qq.com",
				"_xsrf" : "464d07628dc5d61f9dfb9b4ae5d33838",
				"password" : "amwihihc",
				"remember_me" : "true"
				},
			headers = self.headers,
			cookies = self.cookie,
			callback = self.after_login)]

	def after_login(self, response):
		"""after_login."""
		for url in self.start_urls:
			yield self.make_requests_from_url(url, callback = self.parse_topic_page)

	def make_requests_from_url(self, url, **kwargs):
		"""make_requests_from_url."""
		if 'cookies' not in kwargs:
			kwargs['cookies'] = self.cookie
		if 'headers' not in kwargs:
			kwargs['headers'] = self.headers
		kwargs['dont_filter'] = True
		return scrapy.Request(url, **kwargs)

	def parse_page(self, response):
		"""parse_page."""
		# print response.body
		pass

	def parse(self, response):
		"""parse."""
		# print response.body
		pass

	def parse_topic_page(self, response):
		"""parse_topic_page.

		Get all topics url.
		"""
		selector = scrapy.Selector(response)
		# self.topic_offset = self.extract_topic_item(selector)

		try:
			init_list_data_str = selector.xpath('//div[re:test(@class, "zh-general-list")]/@data-init').extract()[0]
			init_list_data_dict = json.loads(init_list_data_str)
			init_list_data_str = None

			xsrf_str = selector.xpath('//input[re:test(@name, "_xsrf")]/@value').extract()[0]
		except Exception, e:
			print "PARSE_TOPIC_PAGE Error", e
			return

		nodename = init_list_data_dict['nodename']
		node_url = "https://www.zhihu.com/node/" + nodename
		params = init_list_data_dict['params']

		for offset in range(0, 650, 20):
			yield self.try_get_next_topic_page(node_url, params, xsrf_str, offset)

	def try_get_next_topic_page(self, url, params, _xsrf, offset):
		params['offset'] = offset
		return scrapy.FormRequest(
			url,
			formdata = {"method" : "next", "params" : json.dumps(params), "_xsrf" : _xsrf},
			headers = self.headers,
			cookies = self.cookie,
			callback = self.next_topic_page)

	def next_topic_page(self, response):
		""" next_topic_page """
		try:
			result_dict = json.loads(response.body)
			result_code = result_dict.get('r', 0)
			if result_code != 0:
				return
			for msg in result_dict.get('msg', []):
				selector = scrapy.Selector(text = msg)
				for request in self.extract_topic_item(selector):
					yield request

		except Exception, e:
			print 'NEXT_TOPIC_PAGE Error', e

	def extract_topic_item(self, selector):
		topic_hrefs = []
		for scope in selector.xpath('//div[re:test(@class, "item")]'):
			topicItem = ZhihuTopicItem()

			topicItem['href'] = ''.join(scope.xpath('./div//a[contains(@href, "topic")]/@href').extract())
			topicItem['img'] = ''.join(scope.xpath('./div//img/@src').extract())
			topicItem['title'] = ''.join(scope.xpath('./div//strong/text()').extract())
			topicItem['desc'] = ''.join(scope.xpath('./div/p/text()').extract())
			topic_hrefs.append(topicItem['href'])
			yield topicItem

		for href in topic_hrefs:
			url = 'https://www.zhihu.com' + href
			yield self.make_requests_from_url(url, callback = self.parse)
