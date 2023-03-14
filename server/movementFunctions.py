from authenticanFunctions import *
from sys import exit
import itertools
import constants


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


def pickup_message(conn):
    send_message(conn, constants.SERVER_PICK_UP)
    send_message(conn, constants.SERVER_LOGOUT)


def at_origin(conn, x, y):
    if x == 0 and y == 0:
        pickup_message(conn)
        exit()


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
