import constants
import itertools
import time
import constants
import socket

LIST_PACKETS = []
LIST_MERGED = []
SUFFIX = '\a\b'


def merging(string):
    global LIST_MERGED
    global SUFFIX
    LIST_MERGED = string.split(SUFFIX)
    LIST_MERGED.pop()
    print(LIST_MERGED)

    if len(LIST_MERGED) == 1:
        return 0
    else:
        return 1


def extractData(conn):
    global SUFFIX
    global LIST_PACKETS
    global LIST_MERGED

    if len(LIST_PACKETS) == 0:
        PACKET = conn.recv(1024).decode()
        LIST_PACKETS = PACKET.split(SUFFIX)
        LIST_PACKETS.pop()

    if len(LIST_MERGED) == 0:
        if len(LIST_PACKETS) == 0:
            # combining segmented data packets
            while (PACKET.endswith(SUFFIX) != True):
                TEMP_PACKET = conn.recv(1024).decode()
                PACKET += TEMP_PACKET

            LIST_PACKETS.append(PACKET)
            DATA_MESSAGE = LIST_PACKETS[0]
            del LIST_PACKETS[0]
            STATUS = merging(DATA_MESSAGE)
            if STATUS == 0:
                del LIST_MERGED[0]
                return DATA_MESSAGE.rstrip(SUFFIX)
        else:
            DATA_MESSAGE = LIST_PACKETS[0]
            del LIST_PACKETS[0]
            return DATA_MESSAGE.rstrip(SUFFIX)

    DATA_MESSAGE = LIST_MERGED[0]
    del LIST_MERGED[0]
    return DATA_MESSAGE.rstrip(SUFFIX)


def keyInRange(key_id):
    if key_id < 0 or key_id > 4:
        return False
    return True


def clientUserNameHashCode(username, key_id, conn):
    key_id = int(key_id)

    if keyInRange(key_id) == False:
        conn.send(constants.SERVER_KEY_OUT_OF_RANGE_ERROR.encode())
        conn.close()

    try:
        hashcode = 0
        for i in range(len(username)):
            hashcode += ord(username[i])

        hashcode *= 1000
        hashcode %= 65536
        expected = hashcode

        server_key = constants.SERVER_CLIENT_KEYS[key_id]['Server Key']
        client_key = constants.SERVER_CLIENT_KEYS[key_id]['Client Key']

        hashcode = (hashcode + server_key) % 65536
        expected = (expected + client_key) % 65536

        hashcode = str(hashcode) + '\a\b'
        return expected, hashcode

    except KeyError as e:
        print(f"Error: {e}")
        return None, None


def hashCompare(hash1, hash2):
    # hash1 is the actual returned hash from the client
    hash1 = int(hash1)
    return constants.SERVER_OK if hash1 == hash2 else constants.SERVER_LOGIN_FAILED


def return_hash(conn):
    # closing the connection if client confirmation is not sent within 1 second
    conn.settimeout(constants.TIMEOUT)
    try:
        return extractData(conn)
    except socket.timeout:
        conn.close()


# Sending Suitable Client Confirmation Message
def client_confirmation_message(conn, returnHash, expectedHashReturn):
    try:
        CLIENT_CONFIRMATION_MESSAGE = hashCompare(
            returnHash, expectedHashReturn)

        if CLIENT_CONFIRMATION_MESSAGE == constants.SERVER_LOGIN_FAILED:
            conn.send(CLIENT_CONFIRMATION_MESSAGE.encode())
            conn.close()
            return False
        else:
            conn.send(CLIENT_CONFIRMATION_MESSAGE.encode())
            return True
    except Exception as e:
        conn.close()
        return False


def authentication(conn):

    CLIENT_USERNAME = extractData(conn)

    # Sending SERVER_KEY_REQUEST
    conn.send(constants.SERVER_KEY_REQUEST.encode())

    # Getting CLIENT_KEY_ID
    CLIENT_KEY_ID = extractData(conn)

    # calculating hashcode of username
    expectedHashReturn, usernameHash = clientUserNameHashCode(
        CLIENT_USERNAME, CLIENT_KEY_ID, conn)

    # sending resultant hashcode to client
    conn.send(usernameHash.encode())

    returnHash = return_hash(conn)

    # If Log In Fails -> close the server
    client_confirmation_message(conn, returnHash, expectedHashReturn)


def pickup_message(conn):
    conn.send(constants.SERVER_PICK_UP.encode())
    conn.send(constants.SERVER_LOGOUT.encode())
    time.sleep(constants.TIMEOUT_PRECISION)


def handleMovement(conn):
    conn.send(constants.SERVER_MOVE.encode())
    coordinates = extractData(conn)

    x = int(coordinates.split()[1])
    y = int(coordinates.split()[2])

    if (y > 0):
        for _ in itertools.repeat(None, y):
            conn.send(constants.SERVER_MOVE.encode())
            time.sleep(constants.TIMEOUT_PRECISION)
            y -= 1

    if (x > 0):
        conn.send(constants.SERVER_TURN_RIGHT.encode())
        for _ in itertools.repeat(None, x):
            conn.send(constants.SERVER_MOVE.encode())
            time.sleep(constants.TIMEOUT_PRECISION)
            x -= 1

    if (x == 0 and y == 0):
        pickup_message(conn)
