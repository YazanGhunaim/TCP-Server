from constants import *


def server_confirmation(conn):
    confirmation_code = 12345
    confirmation_message = f"{confirmation_code}\a\b"
    conn.send(confirmation_message.encode('utf-8'))
