from authenticanFunctions import *
from sys import exit
import constants


def at_origin(conn, x, y):
    if x == 0 and y == 0:
        pickup_message(conn)
        exit()


def zero_check(x, y):
    if x == 0 or y == 0:
        return True
    return False


def extract_coordinates(conn):
    coordinates = extractData(conn)
    x = int(coordinates.split()[1])
    y = int(coordinates.split()[2])
    return x, y


def instant_obstacle(conn):
    send_message(conn, constants.SERVER_TURN_RIGHT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_TURN_LEFT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_TURN_LEFT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_TURN_RIGHT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    return x, y


def evade_obstacle(conn):
    send_message(conn, constants.SERVER_TURN_LEFT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_TURN_RIGHT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_TURN_RIGHT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    send_message(conn, constants.SERVER_TURN_LEFT)
    x, y = extract_coordinates(conn)
    at_origin(conn, x, y)

    return x, y


def fix_orientation_to_y(conn, x, y):
    send_message(conn, constants.SERVER_MOVE)
    new_x, new_y = extract_coordinates(conn)
    at_origin(conn, new_x, new_y)

    # if we encounter an obstacle at this stage
    if x == new_x and y == new_y:
        new_x, new_y = instant_obstacle(conn)

    if new_x > x:
        # facing east
        if new_x > 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
            send_message(conn, constants.SERVER_TURN_LEFT)
            return new_x, new_y, "CHANGED"
        else:
            return new_x, new_y, "CHANGED"
    elif new_x < x:
        # facing west
        if new_x < 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)
            send_message(conn, constants.SERVER_TURN_RIGHT)
            return new_x, new_y, "CHANGED"
        else:
            return new_x, new_y, "CHANGED"

    return new_x, new_y, "UNCHANGED"


def fix_orientation_to_x(conn, x, y):
    send_message(conn, constants.SERVER_MOVE)
    new_x, new_y = extract_coordinates(conn)
    at_origin(conn, new_x, new_y)

    # if we encounter an obstacle at this stage
    if x == new_x and y == new_y:
        new_x, new_y = instant_obstacle(conn)

    elif new_y > y:
        # facing north
        if new_y > 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)
            send_message(conn, constants.SERVER_TURN_RIGHT)
            return new_x, new_y, "CHANGED"
        else:
            return new_x, new_y, "CHANGED"
    elif new_y < y:
        # facing south
        if new_y < 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
            send_message(conn, constants.SERVER_TURN_LEFT)
            return new_x, new_y, "CHANGED"
        else:
            return new_x, new_y, "CHANGED"

    return new_x, new_y, "UNCHANGED"


def get_x_to_zero(conn, x, y):
    x = x
    y = y
    new_y = y
    new_x = x

    while new_x != 0:
        prev_x = new_x
        prev_y = new_y

        send_message(conn, constants.SERVER_MOVE)
        new_x, new_y = extract_coordinates(conn)
        new_x = new_x
        new_y = new_y

        if prev_x == new_x and prev_y == new_y:
            new_x, new_y = evade_obstacle(conn)
            new_x = new_x
            new_y = new_y

        at_origin(conn, new_x, new_y)


def get_y_to_zero(conn, x, y):
    y = y
    x = x
    new_x = x
    new_y = y

    while new_y != 0:
        prev_x = new_x
        prev_y = new_y

        send_message(conn, constants.SERVER_MOVE)
        new_x, new_y = extract_coordinates(conn)
        new_x = new_x
        new_y = new_y

        if prev_x == new_x and prev_y == new_y:
            new_x, new_y = evade_obstacle(conn)
            new_x = new_x
            new_y = new_y

        at_origin(conn, new_x, new_y)


def pickup_message(conn):
    send_message(conn, constants.SERVER_PICK_UP)
    send_message(conn, constants.SERVER_LOGOUT)


def handleMovement(conn):
    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)

    # if already at origin
    at_origin(conn, x, y)

    new_x, new_y, status = fix_orientation_to_y(conn, x, y)
    at_origin(conn, x, y)

    if status == "UNCHANGED":
        new_x, new_y, status = fix_orientation_to_x(conn, new_x, new_y)
        get_y_to_zero(conn, new_x, new_y)
        if new_x > 0 and new_y > 0 or new_y < 0 and new_x < 0:
            send_message(conn, constants.SERVER_TURN_RIGHT)
        else:
            send_message(conn, constants.SERVER_TURN_LEFT)
        new_x, new_y = extract_coordinates(conn)
        get_x_to_zero(conn, new_x, new_y)
    else:
        get_x_to_zero(conn, new_x, new_y)
        if new_x > 0 and new_y > 0 or new_y < 0 and new_x < 0:
            send_message(conn, constants.SERVER_TURN_LEFT)
        else:
            send_message(conn, constants.SERVER_TURN_RIGHT)
        new_x, new_y = extract_coordinates(conn)
        get_y_to_zero(conn, new_x, new_y)
