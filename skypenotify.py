#!/usr/bin/python2
import socket
import sys

def getUnreadCount(sock):
	sock.sendall('unread\n')
	return str(sock.recv(32)).strip()

def getOnlineList(sock):
	sock.sendall('online\n')
	return '\n'.join(str(sock.recv(4096)).split("\x1F"))

def closeServer(sock):
	sock.sendall('close\n')
	return 'closed server'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',9992))

print {
	'--unread':getUnreadCount,
	'--online':getOnlineList,
	'--close':closeServer,
}[sys.argv(1)](sock)
