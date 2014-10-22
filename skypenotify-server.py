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

	def __init__(self, client, port, mintime = 1000):
		self.skype = client
		self.port  = port	

		self.socket = self.initSocket()

		self.online_cache = self.getOnlineList()
		self.unread_cache = self.getUnreadCount()
		self.mintime      = mintime
		self.times	  = {'online':curtime(),'unread':curtime()}

	def initSocket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SO_REUSEADDR)
		s.bind(('',self.port))
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
			lines = str(connection.recv(128)).split('\n')
			print lines
			for text in lines:
				if text == 'unread':
					self.sendUnread()
				elif text == 'online':
					self.sendOnline()
				elif text == 'clear':
					self.clearUnread()
				elif text == 'close':
					self.socket.close()
					sys.exit(0)
					
	def sendUnread(self):
		if self.mininterval('unread'):
			self.unread_cache = self.getUnreadCount()
		socket.send(str(self.unread_cache) + "\n")
	
	def sendOnline(self):
		if mininterval('online'):
			self.online_cache = self.getOnlineList()
		socket.send('\x1F'.join(self.online_cache) + "\n")
	
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
