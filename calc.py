from math import atan2, sqrt, degrees, pi, tan, cos, sin, asin, atan
from re import match
from numpy import polyfit, poly1d, array

# Nato mils conversion rate
milF = 360 / 6400

# Gravitation
g = 9.8

# Velocity approximation guiding values from the game
squadTable = {50: 1579,
              100: 1558,
              150: 1538,
              200: 1517,
              250: 1496,
              300: 1475,
              350: 1453,
              400: 1431,
              450: 1409,
              500: 1387,
              550: 1364,
              600: 1341,
              650: 1317,
              700: 1292,
              750: 1267,
              800: 1240,
              850: 1212,
              900: 1183,
              950: 1152,
              1000: 1118,
              1050: 1081,
              1100: 1039,
              1150: 988,
              1200: 918,
              1250: 800}

'''
Conversions between degrees, mils and radians.
'''


def mil_to_deg(mil):
    return mil * milF


def deg_to_rad(deg):
    return (deg * pi) / 180


def rad_to_deg(rad):
    return (rad * 180) / pi


def deg_to_mil(deg):
    return deg / milF


def rad_to_mil(rad):
    return deg_to_mil(rad_to_deg(rad))


def mil_to_rad(mil):
    return deg_to_rad(mil_to_deg(mil))


''' 
Ballistic Calculations to get different Bullet attributes. Such as time to impact (getTime), 
distance projectile travels (getDist), velocity ot projectile required for distance with given angle (getVel),
angle required to hit target with given velocity, distance and height difference (findAngle)
'''


def get_time(x, rad):
    return sqrt((2 * x * tan(rad)) / g)


def get_dist(v, rad):
    return (tan(rad) * 2 * v * v * cos(rad) * cos(rad)) / g


def get_vel(x, rad):
    return sqrt((x * x * g) / (x * sin(2 * rad)))


def get_angle(x, v):
    return 0.5 * asin((g * x) / (v * v))


def find_angle(x, y, v):
    p1 = sqrt(v ** 4 - g * (g * x ** 2 + 2 * y * v ** 2))
    return atan((v ** 2 + p1) / (g * x))


'''
Splits in game coordinates into easily identifiably string pairs.
'''


def split_cord(cord):
    m = match('^([A-Pa-p])(1[0-6]|0[1-9])-([1-9])-([1-9])$', cord)

    if m is None or len(m.groups()) != 4:
        raise ValueError
    else:
        return m.groups()


'''
Converts string pairs into a coordinate system in metres on which you can do the other calculations.
'''


def look_up(split_cords):
    keys_horizontal = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    keys_horizontal2 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]
    keys_vertical = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
    items_x = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500]
    items_y = [4500, 4200, 3900, 3600, 3300, 3000, 2700, 2400, 2100, 1800, 1500, 1200, 900, 600, 300, 0]
    keys_x = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
    keys_y = ['7', '4', '1', '8', '5', '2', '9', '6', '3']

    items_num_x = [0, 100, 200, 0, 100, 200, 0, 100, 200]
    items_num_y = [200, 100, 0, 200, 100, 0, 200, 100, 0]

    items_num2_x = [0, 33, 66, 0, 33, 66, 0, 33, 66]
    items_num2_y = [66, 33, 0, 66, 33, 0, 66, 33, 0]

    horizontal_look = dict(zip(keys_horizontal, items_x))
    horizontal_look.update(dict(zip(keys_horizontal2, items_x)))
    vertical_look = dict(zip(keys_vertical, items_y))

    numpad1_x = dict(zip(keys_x, items_num_x))
    numpad1_y = dict(zip(keys_y, items_num_y))
    numpad2_x = dict(zip(keys_x, items_num2_x))
    numpad2_y = dict(zip(keys_y, items_num2_y))

    try:
        x1 = horizontal_look[split_cords[0]]
        y1 = vertical_look[split_cords[1]]
        x2 = numpad1_x[split_cords[2]]
        y2 = numpad1_y[split_cords[2]]
        x3 = numpad2_x[split_cords[3]]
        y3 = numpad2_y[split_cords[3]]
    except(IndexError, KeyError):
        raise ValueError

    x_total = x1 + x2 + x3
    y_total = y1 + y2 + y3
    cord = [x_total, y_total]
    return cord


'''
Get the distance and angle (in radian) from two given coordinates in a x y coordinate system.
For compass heading the angle has to be converted to degrees and adjusted to north.
'''


def distance_heading_calc(cords1, cords2):
    distance = sqrt(((cords1[0] - cords2[0]) ** 2) + ((cords1[1] - cords2[1]) ** 2))

    xl = cords2[0] - cords1[0]
    yl = cords2[1] - cords1[1]
    radian = atan2(yl, xl)
    return distance, radian


'''
The coordinates are first converted with the lookUp and splitCord functions (further details there)
and then the angle (in radian and the distance are computed. 
Everything including the converted coordinates are exported as a list.
'''


def get_cords_base_units(cords, i=1):
    distance_int, radian = distance_heading_calc(cords[0], cords[i])
    base_list = [distance_int, radian]
    return base_list


'''
Approximates curve around guiding values (angle for distance). 
And finds angel for given distance using the approximated curve.
'''


def find_closest(table, given_dist):
    np_x = array(list(table.keys()))
    np_y = array(list(table.values()))
    p = poly1d(polyfit(np_x, np_y, 15))
    return get_vel(given_dist, mil_to_rad(p(given_dist)))


'''
Finds mil adjustment for firring mortar with a given distance and height difference.
'''


def mils_calc(dist, height):
    vel = find_closest(squadTable, dist)
    angle = find_angle(dist, int(height), vel)
    return round(rad_to_mil(angle)), get_time(dist, angle)


'''
Convert radians to degrees relative to north (up).
'''


def angle_deg_north(angle):
    return (90 - degrees(angle)) % 360
