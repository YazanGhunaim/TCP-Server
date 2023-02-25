import socket
import threading
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
    conn.settimeout(10)
    try:
        CLIENT_USERNAME = conn.recv(1024).decode()

        # Sending SERVER_KEY_REQUEST
        conn.send(SERVER_KEY_REQUEST.encode())

        # Getting CLIENT_KEY_ID
        CLIENT_KEY_ID = conn.recv(1024).decode()

        # calculating hashcode of username
        expectedHashReturn, usernameHash = clientUserNameHashCode(
            CLIENT_USERNAME, CLIENT_KEY_ID)

        # sending resultant hashcode to client
        conn.send(usernameHash.encode())
        returnHash = conn.recv(1024).decode()

        # Sending Suitable Client Confirmation Message
        CLIENT_CONFIRMATION_MESSAGE = hashCompare(returnHash, expectedHashReturn)

        # If Log In Fails -> close the server
        if CLIENT_CONFIRMATION_MESSAGE == SERVER_LOGIN_FAILED:
            conn.send(CLIENT_CONFIRMATION_MESSAGE.encode())
            conn.close()
        else:
            conn.send(CLIENT_CONFIRMATION_MESSAGE.encode())

        # Commanding the Robot Client To Move
        conn.send(SERVER_MOVE.encode())
        # Recieving robot co-ordinates
        coordinates = conn.recv(1024).decode()
        x, y = extractCoordinates(coordinates)

        if x == 0 and y == 0:
            conn.send(SERVER_PICK_UP.encode())

        # Commanding Client to log out after secret message discovery
        conn.send(SERVER_LOGOUT.encode())

        conn.close()
        return

    except socket.timeout as e:
        print("Timeout!")
        conn.close()


def start():
    server.listen(10)
    while True:
        try:
            conn, address = server.accept()
            thread = threading.Thread(
                target=handle_client, args=(conn, address))
            thread.start()
        except socket.error as e:
            print(f"Error accepting connection: {e}")


start()
