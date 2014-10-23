#!/usr/bin/python2
import Skype4Py
import sys
import socket
import time

def log(msg):
	print >> sys.stderr, str(msg)
def curtime():
	return int(round(time.time() * 1000))

class NotifyServer:

	def __init__(self, client, port, mintime = 5000):
		self.skype = client
		self.port  = port	

		self.socket = self.initSocket()

		self.online_cache = self.getOnlineList()
		self.unread_cache = self.getUnreadCount()

		self.mintime      = mintime
		self.times	  = {'online':curtime(),'unread':curtime()}

	def initSocket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind(('',self.port))
		log('socket initialized')
		return s

	def mininterval(self, field):
		ntime = curtime()
		if ntime - self.times[field] > self.mintime:
			self.times[field] = ntime
			return True
		return False
	
	def run(self):
		self.socket.listen(5)
		while 1:
			connection,addr = self.socket.accept()
			text = str(self.recvall(connection)).strip()
			if text == 'u':
				self.sendUnread(connection)
			elif text == 'o':
				self.sendOnline(connection)
			elif text == 'c':
				self.clearUnread()
			elif text == 'x':
				self.socket.close()
				log('closing server')
				sys.exit(0)
			connection.close()

	def recvall(self, connection):
		data = connection.recv(1024)
		log(data.strip())
		return data

	def sendUnread(self, connection):
		if self.mininterval('unread'):
			self.unread_cache = self.getUnreadCount()
		connection.sendall(str(self.unread_cache) + "\n")
	
	def sendOnline(self, connection):
		#if self.mininterval('online'):
		self.online_cache = self.getOnlineList()
		connection.sendall('\x1F'.join(self.online_cache) + "\n")
	
	def clearUnread(self):
		for msg in self.skype.MissedMessages:
			msg._SetSeen(True)

	def getUnreadCount(self):
		return	self.skype.MissedMessages.Count

	def getOnlineList(self):
		# unreliable for some reason; randomly doesn't work
		return [ user.DisplayName for user in self.skype.Friends
				if user.OnlineStatus != Skype4Py.cusOffline]	

skype = Skype4Py.Skype()
skype.Attach()

NotifyServer(skype, 9992).run()
