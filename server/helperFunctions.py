from constants import *


def clientUserNameHashCode(username, key_id):
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

    return expected, hashcode


def hashCompare(hash1, hash2):
    return SERVER_OK if hash1 == hash2 else SERVER_LOGIN_FAILED
