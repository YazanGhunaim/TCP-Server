import constants
import itertools
import time
import constants
import socket
import sys

LIST_PACKETS = []
LIST_MERGED = []
PACKET_SIZE = 1024
SUFFIX = '\a\b'


def recieve_message(conn):
    conn.settimeout(constants.TIMEOUT)
    return conn.recv(PACKET_SIZE).decode()


def send_message(conn, command):
    time.sleep(constants.TIMEOUT_PRECISION)
    conn.sendall(command.encode())


def merging(string):
    global LIST_MERGED
    global SUFFIX
    LIST_MERGED = string.split(SUFFIX)
    LIST_MERGED.pop()

    if len(LIST_MERGED) == 1:
        return 0
    else:
        return 1


def initialize_packetlist(conn):
    global LIST_PACKETS
    PACKET = recieve_message(conn)
    LIST_PACKETS = PACKET.split(SUFFIX)
    LIST_PACKETS.pop()
    return PACKET


def return_from_merged_list():
    global LIST_MERGED
    global SUFFIX
    DATA_MESSAGE = LIST_MERGED[0]
    del LIST_MERGED[0]
    return DATA_MESSAGE.rstrip(SUFFIX)


def return_from_packet_list():
    global LIST_PACKETS
    global SUFFIX
    DATA_MESSAGE = LIST_PACKETS[0]
    del LIST_PACKETS[0]
    return DATA_MESSAGE.rstrip(SUFFIX)


def combining_segmented_packets(conn, PACKET):
    global LIST_PACKETS
    global LIST_MERGED
    global SUFFIX

    # combining segmented data packets
    while (PACKET.endswith(SUFFIX) != True):
        TEMP_PACKET = recieve_message(conn)
        PACKET += TEMP_PACKET

    LIST_PACKETS.append(PACKET)
    DATA_MESSAGE = LIST_PACKETS[0]
    del LIST_PACKETS[0]

    # merging returns 0 if the data recieved wasnt merged with other packets
    STATUS = merging(DATA_MESSAGE)
    if STATUS == 0:
        del LIST_MERGED[0]
        return DATA_MESSAGE.rstrip(SUFFIX)
    else:
        return return_from_merged_list()


def extractData(conn):
    global SUFFIX
    global LIST_PACKETS
    global LIST_MERGED

    if len(LIST_PACKETS) == 0 and len(LIST_MERGED) == 0:
        PACKET = initialize_packetlist(conn)

    if len(LIST_MERGED) == 0:
        if len(LIST_PACKETS) == 0:
            return combining_segmented_packets(conn, PACKET)
        else:
            return return_from_packet_list()
    else:
        return return_from_merged_list()


def keyInRange(key_id):
    if key_id < 0 or key_id > 4:
        return False
    return True


def clientUserNameHashCode(username, key_id, conn):
    key_id = int(key_id)

    if keyInRange(key_id) == False:
        send_message(conn, constants.SERVER_KEY_OUT_OF_RANGE_ERROR)
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
            send_message(conn, CLIENT_CONFIRMATION_MESSAGE)
            conn.close()
            return False
        else:
            send_message(conn, CLIENT_CONFIRMATION_MESSAGE)
            return True
    except Exception as e:
        conn.close()
        return False


def authentication(conn):

    CLIENT_USERNAME = extractData(conn)

    # Sending SERVER_KEY_REQUEST
    send_message(conn, constants.SERVER_KEY_REQUEST)

    # Getting CLIENT_KEY_ID
    CLIENT_KEY_ID = extractData(conn)

    # calculating hashcode of username
    expectedHashReturn, usernameHash = clientUserNameHashCode(
        CLIENT_USERNAME, CLIENT_KEY_ID, conn)

    # sending resultant hashcode to client
    send_message(conn, usernameHash)

    returnHash = return_hash(conn)

    # If Log In Fails -> close the server
    client_confirmation_message(conn, returnHash, expectedHashReturn)


def pickup_message(conn):
    send_message(conn, constants.SERVER_PICK_UP)
    send_message(conn, constants.SERVER_LOGOUT)


def fix_orientation(conn, x, y):
    send_message(conn, constants.SERVER_MOVE)
    coordinates = extractData(conn)

    new_x = int(coordinates.split()[1])
    new_y = int(coordinates.split()[2])

    if new_x > x:
        # facing east
        if new_x > 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
            send_message(conn, constants.SERVER_TURN_LEFT)
            STATUS = 'x'
            return new_x, new_y, STATUS
        else:
            STATUS = 'x'
            return new_x, new_y, STATUS
    elif new_x < x:
        # facing west
        if new_x < 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)
            send_message(conn, constants.SERVER_TURN_RIGHT)
            STATUS = 'x'
            return new_x, new_y, STATUS
        else:
            STATUS = 'x'
            return new_x, new_y, STATUS
    elif new_y > y:
        # facing north
        if new_y > 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)
            send_message(conn, constants.SERVER_TURN_RIGHT)
            STATUS = 'y'
            return new_x, new_y, STATUS
        else:
            STATUS = 'y'
            return new_x, new_y, STATUS
    elif new_y < y:
        # facing south
        if new_y < 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
            send_message(conn, constants.SERVER_TURN_LEFT)
            STATUS = 'y'
            return new_x, new_y, STATUS
        else:
            STATUS = 'y'
            return new_x, new_y, STATUS


def get_x_to_zero(conn, x, y):
    for _ in itertools.repeat(None, x):
        send_message(conn, constants.SERVER_MOVE)


def get_y_to_zero(conn, x, y):
    for _ in itertools.repeat(None, y):
        send_message(conn, constants.SERVER_MOVE)


def at_origin(conn, x, y):
    if x == 0 and y == 0:
        pickup_message(conn)
        sys.exit()


def handleMovement(conn):
    send_message(conn, constants.SERVER_MOVE)
    coordinates = extractData(conn)

    x = int(coordinates.split()[1])
    y = int(coordinates.split()[2])

    # if already at origin
    at_origin(conn, x, y)

    new_x, new_y, STATUS = fix_orientation(conn, x, y)
    at_origin(conn, x, y)

    if STATUS == 'x':
        get_x_to_zero(conn, new_x, new_y)
        if x < 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
        if x > 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)
        get_y_to_zero(conn, new_x, new_y)
    else:
        get_y_to_zero(conn, new_x, new_y)

        if y < 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
        elif y > 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)

        get_x_to_zero(conn, new_x, new_y)
        pickup_message(conn)
