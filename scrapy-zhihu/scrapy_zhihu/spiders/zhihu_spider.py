#!/usr/bin/python
# -*- encoding=utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
import scrapy

class SpiderZhihu(CrawlSpider):
	name = 'zhihu'

	allowed_domains = ['www.zhihu.com']
        start_urls = [
            'http://www.zhihu.com'
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


	def parse(self, response):
        """ """
        pass

        def start_requests(self):
            return [scrapy.FormRequest(
                "http://www.zhihu.com/login/email",
                formdata = {"email" : "767806886@qq.com",
                    "_xsrf" : "464d07628dc5d61f9dfb9b4ae5d33838",
                    "password" : "amwihihc",
                    "remember_me" : "true"
                    },
                cookies = self.cookie,
                callback = self.after_login)]

        def after_login(self, response):
            print 'after_login', '>' * 30
            pass
