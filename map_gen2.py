import numpy as np
import math
PI = math.pi
markers = []  # (id, x, y, yaw, size)


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return round(qx, 3), round(qy, 3)


def gen_rect(st_p=(0, 0), first=[], count=10, rot=0, size=0.22, mark_sep=0.3):
    rect_markers = []
    map_arr = []
    for i in range(count):
        a = []
        a = first.copy()

        for j in range(len(a)):
            a[j] += len(first)*i
        map_arr.append(a)

    x_or = ((len(map_arr[0])-1) * mark_sep) / 2
    y_or = ((len(map_arr)-1)*mark_sep) / 2
    if rot == 0:
        x_or = 0
        y_or = 0
    for i in range(len(map_arr)-1, -1,  -1):
        for j in range(len(map_arr[i])-1, -1, -1):

            x = round(j*mark_sep, 2)
            y = round((len(map_arr)-i-1)*mark_sep, 2)
            x, y = rotate((0, 0), (x, y), rot)
            m_id = map_arr[i][j]
            rect_markers.append((m_id, x+st_p[0], y+st_p[1], rot, size))
    return rect_markers


markers += gen_rect(st_p=(0, 0), first=[90, 91, 92])
# markers += gen_rect(st_p=(-1.5, 4.1+0.9), first=[30, 31, 32], rot=-PI/2)
# markers += gen_rect(st_p= (-1.76, -1), first= [60, 61, 62], rot=-PI/2)

markers += gen_rect(st_p=(0-4*0.3+0.3, 4.1 + 0.6), first=[30, 31, 32], rot=-PI/2)
markers += gen_rect(st_p= (0-4*0.3+0.3, -1-0.6), first= [60, 61, 62], rot=-PI/2)
# markers += gen_rect(st_p=(0, 0), first=[96, 97, 98], rot=90)

markers += [(3, 1.3, -0.7, PI, 0.26)]
markers += [(9, -0.6, -0.7, PI, 0.26)]
markers += [(7, -0.6, 3.26, 0, 0.26)]
markers += [(17, 1.2, 3.26, 0, 0.26)]


print(markers)
f = open("map.txt", "w+")
for m_id, x, y, yaw, mark_size in markers:
    f.write(str(str(m_id) + "\t" + str(mark_size) + "\t" + str(round(x, 2)
                                                               ) + "\t" + str(round(y, 2)) + "\t0\t" + str(round(yaw, 2)) + "\t0\t0\n"))

print(len(markers))


