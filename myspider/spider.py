# -*- encoding=utf-8 -*-
import asyncore, socket
import threading
import sys
import signal
import urllib
import requests
import time
import Queue
from bs4 import BeautifulSoup
import logger
import utils
import telnet

exit = False


def exit_handler(signum, frame):
	global exit
	exit = True
	print 'receive a signum %d, exit: %d' % (signum, exit)

class Spider:

	def __init__(self):
		self.logger = logger.get_logger('NSSpider.NSSpider')
		self.work_queue = Queue.Queue()
		self.work_queue.put('http://www.baidu.com/')

	def setup(self):
		self.logger.debug('debug message')

	def start(self):
		pass

	def run(self):
		global exit
		if not self.work_queue:
			return
		while True:
			if exit or not self.work_queue:
				return
			url = self.work_queue.get(block=True)
			try:
				r = requests.get(url)
			except Exception, e:
				self.logger.exception(e)
				continue
			soup = BeautifulSoup(r.text)
			for link in soup.find_all('a'):
				if link.get('href', None):
					# self.logger.info('extract url:: %s' % link.get('href', ''))
					self.work_queue.put(link.get('href', ''))
			self.work_queue.task_done()


if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_handler)
	spider = Spider()
	spider.setup()
	spider.start()
	spider.run()
