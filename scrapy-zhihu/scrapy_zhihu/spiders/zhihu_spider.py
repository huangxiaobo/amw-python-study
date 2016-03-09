#!/usr/bin/python
# -*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
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
		print response.body

	def parse(self, response):
		"""parse."""
		print response.body

	def parse_topic_page(self, response):
		"""parse_topic_page.

		Get all topics url.
		"""
		topics = []
		selector = scrapy.Selector(response)
		for scope in selector.xpath('//div[re:test(@class, "item")]'):
			topic = {}
			for key, path in {
				'href'	: './div//a[contains(@href, "topic")]/@href',
				'img'	: './div//img/@src',
				'title'	: './div//strong/text()',
				'desc'	: './div/p/text()',
				}.iteritems():
				scope_result = scope.xpath(path).extract()
				topic[key] = scope_result[0].encode('utf-8') if scope_result else ''
			topics.append(topic)

		for topic in topics:
			url = 'https://www.zhihu.com' + topic['href']
			yield self.make_requests_from_url(url, callback = self.parse)

		try:
			init_data_str = selector.xpath('//div[re:test(@class, "zh-general-list")]/@data-init').extract()[0]
			init_data_dict = json.loads(init_data_str)
			init_data_str = None

			xsrf_str = selector.xpath('//input[re:test(@name, "_xsrf")]/@value').extract()[0]
		except:
			return

		nodename = init_data_dict['nodename']
		params = init_data_dict['params']
		yield scrapy.FormRequest(
			"https://www.zhihu.com/node/" + nodename,
			formdata = {"method" : "next", "params" : params, "_xsrf" : xsrf_str},
			headers = self.headers,
			cookies = self.cookie,
			callback = self.next_topic_page)

	def next_topic_page(self, response):
		print response.body
