import os
import socket
import threading
from time import sleep
from constants import *
from helperFunctions import *

HEADER = 64
PORT = 6667
ADDR = ('localhost', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    # fork returns process id of the child - stored in the parent
    child_pid = os.fork()

    connected = True
    while connected:
        if child_pid != 0:  # we are in the parent thread
            conn.close()
            continue

        # server.close()

        print(addr)
        conn.settimeout(10)
        try:
            data = conn.recv(1024).decode()
            print(data)
            sleep(10)
            server_confirmation(conn)
            conn.close()
            break

        except socket.timeout as e:
            print("Timeout!")
            conn.close()


def start():
    server.listen(10)
    while True:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()


start()
