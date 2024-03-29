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
SERVER_PICK_UP = "105 GET MESSAGE\a\b"
SERVER_LOGOUT = "106 LOGOUT\a\b"
SERVER_KEY_OUT_OF_RANGE_ERROR = "303 KEY OUT OF RANGE\a\b"
SERVER_TURN_LEFT = "103 TURN LEFT\a\b"
SERVER_TURN_RIGHT = "104 TURN RIGHT\a\b"
SERVER_SYNTAX_ERROR = "301 SYNTAX ERROR\a\b"
SERVER_LOGIC_ERROR = "302 LOGIC ERROR\a\b"

CLIENT_RECHARGING = "RECHARGING\a\b"
CLIENT_FULL_POWER = "FULL POWER\a\b"
# Time constants
TIMEOUT = 1
TIMEOUT_RECHARGING = 5


# number of bytes of recieved message
PACKET_SIZE = 1024
# termination sequence of packet messages
SUFFIX = '\a\b'
