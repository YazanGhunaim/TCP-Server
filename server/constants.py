# five pairs of authentication keys
SERVER_CLIENT_KEYS = {
    0: {'Server Key': 23019, 'Client Key': 32037},
    1: {'Server Key': 32037, 'Client Key': 29295},
    2: {'Server Key': 18789, 'Client Key': 13603},
    3: {'Server Key': 16443, 'Client Key': 29533},
    4: {'Server Key': 18189, 'Client Key': 21952}
}

SERVER_KEY_REQUEST = "107 KEY REQUEST\a\b"
SERVER_OK = "200 OK\a\b"
SERVER_LOGIN_FAILED = "300 LOGIN FAILED\a\b"
SERVER_MOVE = "102 MOVE\a\b"