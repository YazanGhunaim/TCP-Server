from time import sleep
import socket
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 6667))

s.send(sys.argv[1].encode())

print(s.recv(1024).decode())

s.close()
