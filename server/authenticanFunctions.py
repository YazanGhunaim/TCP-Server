from time import sleep
import validationTests
import constants
import socket

LIST_PACKETS = []
LIST_MERGED = []


def recieve_message(conn):
    conn.settimeout(constants.TIMEOUT)
    try:
        return conn.recv(constants.PACKET_SIZE).decode()
    except socket.timeout:
        conn.close()


def send_message(conn, command):
    sleep(constants.TIMEOUT_PRECISION)
    conn.sendall(command.encode())


def merging(string):
    global LIST_MERGED
    LIST_MERGED = string.split(constants.SUFFIX)
    LIST_MERGED.pop()

    if len(LIST_MERGED) == 1:
        return 0
    else:
        return 1


def initialize_packetlist(conn):
    global LIST_PACKETS
    PACKET = recieve_message(conn)
    LIST_PACKETS = PACKET.split(constants.SUFFIX)
    LIST_PACKETS.pop()
    return PACKET


def return_from_merged_list():
    global LIST_MERGED
    DATA_MESSAGE = LIST_MERGED[0]
    del LIST_MERGED[0]
    return DATA_MESSAGE.rstrip(constants.SUFFIX)


def return_from_packet_list():
    global LIST_PACKETS
    DATA_MESSAGE = LIST_PACKETS[0]
    del LIST_PACKETS[0]
    return DATA_MESSAGE.rstrip(constants.SUFFIX)


def combining_segmented_packets(conn, PACKET):
    global LIST_PACKETS
    global LIST_MERGED

    # combining segmented data packets
    while (PACKET.endswith(constants.SUFFIX) != True):
        TEMP_PACKET = recieve_message(conn)
        PACKET += TEMP_PACKET

    LIST_PACKETS.append(PACKET)
    DATA_MESSAGE = LIST_PACKETS[0]
    del LIST_PACKETS[0]

    # merging returns 0 if the data recieved wasnt merged with other packets
    STATUS = merging(DATA_MESSAGE)
    if STATUS == 0:
        del LIST_MERGED[0]
        return DATA_MESSAGE.rstrip(constants.SUFFIX)
    else:
        return return_from_merged_list()


def extractData(conn):
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
    validationTests.usernameTest(conn, CLIENT_USERNAME)

    # Sending SERVER_KEY_REQUEST
    send_message(conn, constants.SERVER_KEY_REQUEST)

    # Getting CLIENT_KEY_ID
    CLIENT_KEY_ID = extractData(conn)
    validationTests.key_not_number(conn, CLIENT_KEY_ID)

    # calculating hashcode of username
    expectedHashReturn, usernameHash = clientUserNameHashCode(
        CLIENT_USERNAME, CLIENT_KEY_ID, conn)

    # sending resultant hashcode to client
    send_message(conn, usernameHash)

    returnHash = return_hash(conn)
    validationTests.space_confirmation(conn, returnHash)
    validationTests.six_digit_confirmation(conn, returnHash)

    # If Log In Fails -> close the server
    client_confirmation_message(conn, returnHash, expectedHashReturn)
