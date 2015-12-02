#!-*- coding=utf-8 -*-
import logging
import sys


class Logger(object):
	log_modules = set()
	log_level = logging.DEBUG
	logging.basicConfig(filename='log.txt', level=logging.DEBUG)

	@staticmethod
	def get_logger(moduleName):
		if moduleName in Logger.log_modules:
			return logging.getLogger(moduleName)
		logger = logging.getLogger(moduleName)
		# logger.setLevel(logging.DEBUG)

		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		formatter = logging.Formatter(
			'%(asctime)s - %(filename)s - %(lineno)d - %(process)d - %(threadName)s : %(message)s')
		ch.setFormatter(formatter)

		logger.addHandler(ch)

		Logger.log_modules.add(moduleName)
		return logger

get_logger = Logger.get_logger
