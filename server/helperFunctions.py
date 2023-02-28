import constants
import itertools
import time
import constants


def keyInRange(key_id):
    if key_id < 0 or key_id > 4:
        return False
    return True


def clientUserNameHashCode(username, key_id, conn):
    # rstrip method removes any occurences of specified characters then converted to integer
    key_id = int(key_id.rstrip('\a\b'))

    if keyInRange(key_id) == False:
        conn.send(constants.SERVER_KEY_OUT_OF_RANGE_ERROR.encode())
        conn.close()

    try:
        hashcode = 0
        for i in range(len(username) - 2):
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
    hash1 = int(hash1.rstrip('\a\b'))
    return constants.SERVER_OK if hash1 == hash2 else constants.SERVER_LOGIN_FAILED


def authentication(conn):

    CLIENT_USERNAME = conn.recv(1024).decode()

    # Sending SERVER_KEY_REQUEST
    conn.send(constants.SERVER_KEY_REQUEST.encode())

    # Getting CLIENT_KEY_ID
    CLIENT_KEY_ID = conn.recv(1024).decode()

    # calculating hashcode of username
    expectedHashReturn, usernameHash = clientUserNameHashCode(
        CLIENT_USERNAME, CLIENT_KEY_ID, conn)

    # sending resultant hashcode to client
    conn.send(usernameHash.encode())
    returnHash = conn.recv(1024).decode()

    # Sending Suitable Client Confirmation Message
    CLIENT_CONFIRMATION_MESSAGE = hashCompare(
        returnHash, expectedHashReturn)

    # If Log In Fails -> close the server
    if CLIENT_CONFIRMATION_MESSAGE == constants.SERVER_LOGIN_FAILED:
        conn.send(CLIENT_CONFIRMATION_MESSAGE.encode())
        conn.close()
    else:
        conn.send(CLIENT_CONFIRMATION_MESSAGE.encode())


def pickup_message(conn):
    conn.send(constants.SERVER_PICK_UP.encode())
    conn.send(constants.SERVER_LOGOUT.encode())
    time.sleep(constants.TIMEOUT_PRECISION)


def handleMovement(conn):
    conn.send(constants.SERVER_MOVE.encode())
    coordinates = conn.recv(1024).decode()
    x = int(coordinates.split()[1])
    y = int(coordinates.split()[2].rstrip('\a\b'))

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

    pickup_message(conn)
