#!/usr/bin/python2
import socket
import sys

def getUnreadCount(sock):
	sock.sendall('u\n')
	return str(sock.recvfrom(4096)[0]).strip()

def getOnlineList(sock):
	sock.sendall('o\n')
	return '\n'.join(str(sock.recvfrom(4096)[0]).split("\x1F"))

def closeServer(sock):
	sock.sendall('x\n')
	return 'closed server'

def clearMessages(sock):
	sock.sendall('c\n')
	return 'cleared messages'

options = {
	'unread':getUnreadCount,
	'online':getOnlineList,
	'exit':closeServer,
	'clear':clearMessages,
}
def usage():
	print "usage: skypenotify <unread,online,exit,clear> <port (default 9992)>"
	sys.exit(1)

if len(sys.argv) < 2:
	usage()
choice = sys.argv[1]
if not choice in options:
	usage()

port = (len(sys.argv) >= 3) and int(sys.argv[2]) or 9992

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',port))

print options[choice](sock)

sock.close()
