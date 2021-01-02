from math import sin, cos
import calc


def lineFire(target1, target2):
    dist, heading = calc.distance_heading_calc(target1, target2)
    fire_cords = []
    rounds = int(dist // 5) + 1
    for i in range(rounds):
        xl2 = round(10 * i * sin(heading))
        yl2 = round(10 * i * cos(heading))
        fire_cords.append([xl2 + target1[0], yl2 + target1[1]])
    return fire_cords


def areaFire(target1, target2):
    stride_x = 1
    stride_y = 1
    fire_cords = []

    x_dif = target2[0] - target1[0]
    y_dif = target2[1] - target1[1]
    rounds_x = int(x_dif // 5)
    rounds_y = int(y_dif // 5)

    if rounds_x < 0:
        stride_x = -1
        rounds_x -= 1
    else:
        rounds_x += 1
    if rounds_y < 0:
        stride_y = -1
        rounds_y -= 1
    else:
        rounds_y += 1

    for x in range(0, rounds_x, stride_x):
        for y in range(0, rounds_y, stride_y):
            cord = [(target1[0] + 10 * x), (target1[1] + 10 * y)]
            fire_cords.append(cord)

    return fire_cords