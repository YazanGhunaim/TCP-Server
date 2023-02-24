import socket
import threading
from time import sleep
from constants import *
from helperFunctions import *

HEADER = 64
PORT = 5050
ADDR = ('localhost', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(addr)
    conn.settimeout(10)
    try:
        CLIENT_USERNAME = conn.recv(1024).decode()

        # Sending SERVER_KEY_REQUEST
        conn.send(SERVER_KEY_REQUEST.encode())
        conn.close()
        return

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
