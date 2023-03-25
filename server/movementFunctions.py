from authenticanFunctions import *
from validationTests import space_confirmation, float_test
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
    space_confirmation(conn, coordinates)
    x = coordinates.split()[1]
    y = coordinates.split()[2]
    float_test(conn, x, y)
    at_origin(conn, int(x), int(y))
    return int(x), int(y)


def move(conn):
    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)
    return x, y


def turn_left(conn):
    send_message(conn, constants.SERVER_TURN_LEFT)
    x, y = extract_coordinates(conn)
    return x, y


def turn_right(conn):
    send_message(conn, constants.SERVER_TURN_RIGHT)
    x, y = extract_coordinates(conn)
    return x, y


def axis_obstacle(conn, mode):
    # RMLM
    if mode == 1:
        x, y = turn_right(conn)
        x, y = move(conn)
        x, y = turn_left(conn)
        x, y = move(conn)

    # LMRM
    else:
        x, y = turn_left(conn)
        x, y = move(conn)
        x, y = turn_right(conn)
        x, y = move(conn)

    return x, y


def instant_obstacle(conn):
    x, y = turn_right(conn)
    x, y = move(conn)

    return x, y


def evade_obstacle(conn):
    x, y = turn_left(conn)
    x, y = move(conn)
    x, y = turn_right(conn)
    x, y = move(conn)
    x, y = move(conn)
    x, y = turn_right(conn)
    x, y = move(conn)
    x, y = turn_left(conn)

    return x, y


def face_to_x(conn, x, y):
    new_x, new_y = move(conn)

    # if an obstacle is encountered
    if x == new_x and y == new_y:
        new_x, new_y = instant_obstacle(conn)

    if x > 0 and y < 0 or x < 0 and y < 0 or x == 0 and y < 0:

        if new_x == x and new_y > y:
            return new_x, new_y
        elif new_x == x and new_y < y:
            new_x, new_y = turn_left(conn)
            new_x, new_y = turn_left(conn)
        elif new_x > x and new_y == y:
            new_x, new_y = turn_left(conn)
        elif new_x < x and new_y == y:
            new_x, new_y = turn_right(conn)

    elif x > 0 and y > 0 or x == 0 and y > 0 or x < 0 and y > 0:

        if new_x == x and new_y > y:
            new_x, new_y = turn_left(conn)
            new_x, new_y = turn_left(conn)
        elif new_x == x and new_y < y:
            return new_x, new_y
        elif new_x > x and new_y == y:
            new_x, new_y = turn_right(conn)
        elif new_x < x and new_y == y:
            new_x, new_y = turn_left(conn)

    elif x < 0 and y == 0:

        if new_x == x and new_y > y or new_x == x and new_y < y or new_x < x and new_y == y:
            new_x, new_y = turn_left(conn)
            new_x, new_y = turn_left(conn)
        elif new_x > x and new_y == y:
            return new_x, new_y

    elif x > 0 and y == 0:

        if new_x == x and new_y > y or new_x == x and new_y < y or new_x > x and new_y == y:
            new_x, new_y = turn_left(conn)
            new_x, new_y = turn_left(conn)
        elif new_x < x and new_y == y:
            return new_x, new_y
    return new_x, new_y


def get_x_to_zero(conn, x, y):
    new_y = y
    new_x = x

    while new_x != 0:
        prev_x = new_x
        prev_y = new_y

        new_x, new_y = move(conn)

        if prev_x == new_x and prev_y == new_y:
            if new_x + 1 == 0 or new_x - 1 == 0:
                if new_x > 0 and new_y > 0 or new_x < 0 and new_y < 0:
                    new_x, new_y = axis_obstacle(conn, 2)
                else:
                    new_x, new_y = axis_obstacle(conn, 1)
            else:
                new_x, new_y = evade_obstacle(conn)

        at_origin(conn, new_x, new_y)


def get_y_to_zero(conn, x, y):
    count = 0
    new_x = x
    new_y = y

    while new_y != 0:
        count += 1
        prev_x = new_x
        prev_y = new_y

        new_x, new_y = move(conn)

        if prev_x == new_x and prev_y == new_y:
            if new_y + 1 == 0 or new_y - 1 == 0:
                if new_x > 0 and new_y > 0 or new_x < 0 and new_y < 0:
                    new_x, new_y = axis_obstacle(conn, 1)
                else:
                    new_x, new_y = axis_obstacle(conn, 2)
            else:
                new_x, new_y = evade_obstacle(conn)

        at_origin(conn, new_x, new_y)


def pickup_message(conn):
    send_message(conn, constants.SERVER_PICK_UP)
    secret = recieve_message(conn)
    validationTests.secret_length(conn, secret)
    send_message(conn, constants.SERVER_LOGOUT)


def handleMovement(conn):
    send_message(conn, constants.SERVER_MOVE)
    x, y = extract_coordinates(conn)

    new_x, new_y = face_to_x(conn, x, y)
    at_origin(conn, x, y)

    count = get_y_to_zero(conn, new_x, new_y)
    if count == 0:
        if x > 0 and y > 0 or x < 0 and y < 0:
            new_x, new_y = turn_right(conn)
        elif x < 0 and y > 0 or x > 0 and y < 0:
            new_x, new_y = turn_left(conn)
    elif new_x > 0 and new_y > 0 or new_y < 0 and new_x < 0:
        new_x, new_y = turn_right(conn)
    else:
        new_x, new_y = turn_left(conn)
    get_x_to_zero(conn, new_x, new_y)
