#!/usr/bin/python
# encoding=utf-8
import time
import socket
import asyncore
import threading
import select
from cStringIO import StringIO

from NSLogger import NSLogger
import NSConst as NSConst

# 负责接受Client socket的连接



class TelnetServer():
	TIMEOUT = 20

	def __init__(self, host, port):
		self.logger = NSLogger.get_logger('NSServerConsole.TelnetServer')
		self.host = host
		self.port = port
		self.client_id = 1

	def start(self):
		self.logger.debug('start')
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.try_bind()
			self.sock.listen(5)
		except socket.error as msg:
			self.sock.close()
			self.sock = None

		self.w_socks = []
		self.r_socks = [self.sock]
		self.e_socks = []
		self.connections = {}

		while True:
			time.sleep(1)
			self.process()

	def stop(self):
		pass

	def try_bind(self):
		self.logger.debug('try_bind')
		while True:
			try:
				self.sock.bind((self.host, self.port))
				break
			except:
				self.port += 1
				if self.port > 2**16 - 1:
					raise StandardError(
						'TelnetServer failed to find a port to bind')

	def process(self):
		readable, writable, exceptional = select.select(
			self.r_socks, self.w_socks, self.r_socks, TelnetServer.TIMEOUT)
		if not(readable, writable, exceptional):
			self.logger.debug('time out...')
			return
		for s in readable:
			if s is self.sock:
				# 主机
				# 接受连接
				self.handle_accept()
			else:
				# 发来消息
				self.handle_read(s)
		for s in writable:
			self.handle_write(s)
		for s in exceptional:
			self.handle_leave(s)

	def handle_accept(self):
		pair = self.sock.accept()
		if pair is None:
			pass
		else:
			sock, addr = pair
			conn = self._add_client(self.client_id, sock)
			self.client_id += 1
			print 'connect from ', sock.getpeername()
			conn.send_data('hello\r\n')

	def handle_read(self, client):
		conn = self.connections.get(client, None)
		if conn:
			data = conn.handle_read()
			conn.send_data(data)

	def handle_write(self, client):
		conn = self.connections.get(client, None)
		if conn:
			conn.handle_write()

	def handle_leave(self, client):
		self._del_client(client)
		return True

	def _del_client(self, client):
		del self.connections[client]
		self.r_socks.remove(client)
		self.w_socks.remove(client)

	def _add_client(self, client_id, client):
		self.r_socks.append(client)
		self.w_socks.append(client)
		self.connections[client] = TelnetConnection(client_id, client)
		return self.connections[client]


class TelnetConnection(object):
	DEFAULT_RECV_BUFFER = 4096

	def __init__(self, clientid, sock):
		self.logger = NSLogger.get_logger('NSServerConsole.TelnetConnection')
		self.w_buffer = StringIO()
		self.r_buffer = StringIO()
		self.sock = sock
		self.clientid = clientid
		self.clientname = None

	def handle_read(self):
		data = self.sock.recv(TelnetConnection.DEFAULT_RECV_BUFFER)
		if len(data) > 0:
			print 'recv : ', data
		return data

	def handle_write(self):
		buff = self.w_buffer.getvalue()
		if buff:
			sent = self.sock.send(buff)
			self.w_buffer = StringIO()
			self.w_buffer.write(buff[sent:])

	def send_data(self, data):
		data = data.replace('\r\n', '\n').replace('\n', '\r\n')
		self.w_buffer.write(data)

	def test_writable(self):
		return self.w_buffer.getvalue()
