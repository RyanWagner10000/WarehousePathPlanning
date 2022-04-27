import numpy as np
import matplotlib.pyplot as plt
from old_Map import WHMap
import time

# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
AREA_WIDTH = 30.0  # potential area width [m]

show_animation = True


def calc_potential_field(gx, gy, ox, oy, reso, rr):
    minx = min(ox) - AREA_WIDTH / 2.0
    miny = min(oy) - AREA_WIDTH / 2.0
    maxx = max(ox) + AREA_WIDTH / 2.0
    maxy = max(oy) + AREA_WIDTH / 2.0
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        x = ix * reso + minx

        for iy in range(yw):
            y = iy * reso + miny
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap, minx, miny


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * KP * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr):
    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i, _ in enumerate(ox):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1

        return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
    else:
        return 0.0


def get_motion_model():
    # dx, dy
    motion = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]

    return motion


def potential_field_planning(sx, sy, gx, gy, ox, oy, reso, rr):

    # calc potential field
    pmap, minx, miny = calc_potential_field(gx, gy, ox, oy, reso, rr)

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round((sx - minx) / reso)
    iy = round((sy - miny) / reso)
    gix = round((gx - minx) / reso)
    giy = round((gy - miny) / reso)

    if show_animation:
        draw_heatmap(pmap)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(ix, iy, "*k")
        plt.plot(gix, giy, "*m")

    rx, ry = [sx], [sy]
    motion = get_motion_model()
    t = 0
    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]):
                p = float("inf")  # outside area
            else:
                p = pmap[inx][iny]
            if minp > p:
                minp = p
                minix = inx
                miniy = iny
        ix = minix
        iy = miniy
        xp = ix * reso + minx
        yp = iy * reso + miny
        d = np.hypot(gx - xp, gy - yp)
        rx.append(xp)
        ry.append(yp)
        t += 1
        if t > 30:break
        if show_animation:
            plt.plot(ix, iy, ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry


def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)


def main():
    print("potential_field_planning start")
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m]
    for i in range(3):
        # plt.figure()
        start_t = time.time()

        plt.clf()
        env = WHMap()

        j = np.random.randint(0,len(env.x))
        sx = env.x[j]  # start x position [m]
        sy = env.y[j]  # start y positon [m]

        ox = env.ox
        oy = env.oy
        j = np.random.randint(0,len(env.ox))
      # obstacle y position list [m]
        gx = ox[j]  # goal x position [m]
        gy = oy[j]  # goal y position [m]
        ox[j] = ox[0]
        oy[j] = oy[0]

        if show_animation:
            plt.grid(True)
            plt.axis("equal")

        # path generation
        one_x, one_y = potential_field_planning(
            sx, sy, gx, gy, ox, oy, grid_size, robot_radius)
        print('first route is', one_x, one_y)

        if np.linalg.norm([one_x[-1]-gx, one_y[-1]-gy]) < 4:
            j = np.random.randint(0, len(env.x))
            sx = one_x[-1]  # start x position [m]
            sy = one_y[-1]  # start y positon [m]

            ox = env.ox
            oy = env.oy
            j = np.random.randint(0, len(env.gx))
            # obstacle y position list [m]
            gx = env.gx[j]  # goal x position [m]
            gy = env.gy[j]  # goal y position [m]
            one_x, one_y = potential_field_planning(
                sx, sy, gx, gy, ox, oy, grid_size, robot_radius)
        print('second route is', one_x, one_y)
        print('total time of ', str(i), ' is ', time.time() - start_t )
    if show_animation:
        plt.show()


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
