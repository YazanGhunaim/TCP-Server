import socket
import threading

HEADER = 64
PORT = 5050
# get IP address automatically
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# new socket (socket.socket) with family/type AF_INET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding socket to address
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # we will not pass until we recieve a message
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_legnth = int(msg_length)
            msg = conn.recv(msg_legnth).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # we will not pass until we get a connection
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()
