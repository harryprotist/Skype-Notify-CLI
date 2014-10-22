#!/usr/bin/python2
import Skype4Py
import sys
import socket
import time

def log(msg):
	print >> sys.stderr, str(msg)
def curtime():
	int(round(time.time() * 1000))

class NotifyServer:

	def __init__(self, client, port, mintime = 1000):
		self.skype = client
		self.port  = port	

		self.socket = self.initSocket()

		self.online_cache = self.getOnlineList()
		self.unread_cache = self.getUnreadCount()
		self.mintime      = mintime
		self.time	  = 

	def initSocket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(self.port)
		return s
	
	def run(self, frequency):
		self.socket.listen(5)
		while 1:
			connection,addr = self.socket.accept()
			lines = str(connection).split('\n')
			for text in lines:
				if text == 'unread':
					self.sendUnread()
				elif text == 'online':
					self.sendOnline()
				if text == 'clear':
					self.clearUnread()
					
	
	def getUnreadCount(self):
		return	self.skype.MissedMessages.Count

	def getOnlineList(self):
		# unreliable for some reason; randomly doesn't work
		return [ user.DisplayName for user in self.skype.Friends
				if user.OnlineStatus != Skype4Py.cusOffline]	

skype = Skype4Py.Skype()
skype.Attach()

print str(NotifyServer(skype, 9992).getOnlineList())
