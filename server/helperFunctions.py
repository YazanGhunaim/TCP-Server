from constants import *


def keyInRange(key_id):
    if key_id < 0 or key_id > 4:
        return False
    return True


def clientUserNameHashCode(username, key_id, conn):
    # rstrip method removes any occurences of specified characters then converted to integer
    key_id = int(key_id.rstrip('\a\b'))

    if keyInRange(key_id) == False:
        conn.send(SERVER_KEY_OUT_OF_RANGE_ERROR.encode())
        conn.close()

    try:
        hashcode = 0
        for i in range(len(username) - 2):
            hashcode += ord(username[i])

        hashcode *= 1000
        hashcode %= 65536
        expected = hashcode

        server_key = SERVER_CLIENT_KEYS[key_id]['Server Key']
        client_key = SERVER_CLIENT_KEYS[key_id]['Client Key']

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
    return SERVER_OK if hash1 == hash2 else SERVER_LOGIN_FAILED


def extractCoordinates(coordinates):
    x = int(coordinates.split()[1])
    y = int(coordinates.split()[2].rstrip('\a\b'))
    return x, y
