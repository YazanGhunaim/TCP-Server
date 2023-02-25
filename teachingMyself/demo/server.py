import os
import socket
from time import sleep


l = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket creation: ip/tcp
l.bind(('localhost',6667)) #binding the socket to this device, port number 6666
l.listen(10) #number of clients

while True:

    c, address = l.accept() #accept returns newly created socket and address of the client

    child_pid = os.fork() #fork returns process id of the child - stored in the parent

    if child_pid != 0:  #we are in the parent thread
        c.close()
        continue

    l.close()

    print(address)
    c.settimeout(10)
    try:
        data = c.recv(1024).decode() #recv gets sequence of bytes -> decoding into string

        print(data)

        sleep(10) #10 seconds

        c.send("Hello client!".encode())

        c.close()
        break #child executes only one cycle

    except socket.timeout as e: #if timeout occurs
        print("Timeout!")
        c.close()


