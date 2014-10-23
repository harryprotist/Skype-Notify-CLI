#!/usr/bin/python2
import socket
import sys

def getUnreadCount(sock):
	sock.sendall('u\n')
	return str(sock.recvfrom(4096)).strip()

def getOnlineList(sock):
	sock.sendall('o\n')
	return '\n'.join(str(sock.recvfrom(4096)).split("\x1F"))

def closeServer(sock):
	sock.sendall('x\n')
	return 'closed server'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',9992))

print {
	'--unread':getUnreadCount,
	'--online':getOnlineList,
	'--close':closeServer,
}[sys.argv[1]](sock)
sock.close()
