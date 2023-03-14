from authenticanFunctions import authentication
from movementFunctions import handleMovement
from time import sleep
import socket
import threading

PORT = 6666
ADDR = ('localhost', PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    conn.settimeout(10)
    try:

        # commands and packets regarding the robot authentication procedure
        authentication(conn)
        handleMovement(conn)

    except socket.timeout as e:
        print("Timeout!")
        conn.close()
    finally:
        sleep(1)
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
