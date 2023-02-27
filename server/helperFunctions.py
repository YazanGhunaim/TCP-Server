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


def extractCoordinates(coordinates, conn):
    x = int(coordinates.split()[1])
    y = int(coordinates.split()[2].rstrip('\a\b'))
    status = handleMovement(x, y, conn)

    # print(status)
    # if status == True:
        # conn.close()


def handleMovement(x, y, conn):

    if (y > 0):
        while (y != 0):
            print(y)
            y -= 1
            conn.send(constants.SERVER_MOVE.encode())

    if (x > 0):
        conn.send(constants.SERVER_TURN_RIGHT.encode())
        while (x != 0):
            x -= 1
            conn.send(constants.SERVER_MOVE.encode())

    if x == 0 and y == 0:
        conn.send(constants.SERVER_PICK_UP.encode())
        conn.send(constants.SERVER_LOGOUT.encode())
        return True
    else:
        return False
