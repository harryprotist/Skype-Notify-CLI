#!/usr/bin/python2
import Skype4Py
import sys
import socket

def log(msg):
	print >> sys.stderr, str(msg)

class NotifyServer:

	def __init__(self, client, port):
		self.skype = client
		self.port  = port	

	def initSocket(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(self.port)
		return s
	
	def run(self, frequency):
				
	
	def getUnreadCount(self):
		return	self.skype.MissedMessages.Count +
			self.skype.MissedCalls.Count +
			self.skype.MissedChats.Count +
			self.skype.MissedVoicemails.Count	

	def getOnlineList(self):
		return [ user.FullName for user in self.skype.Friends
				if user.OnlineStatus != Skype4Py.cusOffline]	

skype = Skype4Py.Skype()
skype.Attach()
