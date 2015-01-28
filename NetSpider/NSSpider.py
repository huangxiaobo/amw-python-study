import socket
import threading
import sys, urllib
import time
import Queue
from bs4 import BeautifulSoup
from NSLogger import NSLogger
import NSConst
import NSUtils

is_exit = False

def exit_handler(signum, frame):
	global is_exit
	is_exit = True
	print 'receive a signal %d, is_exit: %d' % (signal, is_exit)


class NSSpider:
	def __init__(self):
		self.logger = NSLogger.get_logger('NSSpider.NSSpider')
		self.work_queue = Queue.Queue()
		self.work_queue.put('http://www.baidu.com/')
		# thread pool
		self.pool = [threading.Thread(target = self.process, args = (self.work_queue, )) for _ in range(NSConst.POOL_SIZE)]
		self.pool.append(threading.Thread(target = self.start_telnet_console, args = ()))


	def setup(self):
		self.logger.debug('debug message')
		# self.start_telnet_console()

	def start(self):
		for t in self.pool:
			t.start()
		for t in self.pool:
			t.join()


	def start_telnet_console(self):
		self.logger.debug('_startTelnetConsole')
		#try:
		import NSServerConsole
		self.telnetServer = NSServerConsole.TelnetServer(host = '127.0.0.1', port = 30000)
		self.telnetServer.start()

	def process(self, work_queue):
		if not work_queue:
			return
		while True:
			url = work_queue.get(block = True)
			try:
				# print 'ready to read:', url
				f = urllib.urlopen(url)
			except:
				# print 'urlopen exception'
				continue
			soup = BeautifulSoup(f)
			for link in soup.find_all('a'):
				if link.get('href', None):
					# print link.get('href', '')
					work_queue.put(link.get('href', ''))
			work_queue.task_done()

if __name__ == '__main__':

	spider = NSSpider()
	spider.setup()
	spider.start()
