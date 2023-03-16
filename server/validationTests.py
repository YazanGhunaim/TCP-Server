import authenticanFunctions
import constants


def close_connection(conn):
    conn.close()


def usernameTest(conn, username):
    if not username or len(username) > 18:
        authenticanFunctions.send_message(conn, constants.SERVER_SYNTAX_ERROR)
        close_connection(conn)


def key_not_number(conn, key):
    if not key.isnumeric():
        authenticanFunctions.send_message(conn, constants.SERVER_SYNTAX_ERROR)
        close_connection(conn)


def space_confirmation(conn, confirmation):
    if confirmation.endswith(' '):
        authenticanFunctions.send_message(conn, constants.SERVER_SYNTAX_ERROR)
        close_connection(conn)


def six_digit_confirmation(conn, key):
    if len(key) > 5:
        authenticanFunctions.send_message(conn, constants.SERVER_SYNTAX_ERROR)
        close_connection(conn)


def float_test(conn, x, y):
    if x.find('.') != -1 or y.find('.') != -1:
        authenticanFunctions.send_message(conn, constants.SERVER_SYNTAX_ERROR)
        close_connection(conn)


def suffix_test(conn, packet):
    if packet.split(constants.SUFFIX)[0].endswith("\a"):
        authenticanFunctions.send_message(conn, constants.SERVER_SYNTAX_ERROR)
        close_connection(conn)
