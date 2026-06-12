import matplotlib.pyplot as plt
import numpy as np
import math

def run(config):

    c_re = config.a
    c_im = config.b
    n = config.points

    xmin, xmax = -2, 2
    ymin, ymax = -2, 2

    xs, ys = [], []

    for i in range(n):
        # punto inicial en el plano complejo
        x = np.random.uniform(xmin, xmax)
        y = np.random.uniform(ymin, ymax)

        zx, zy = x, y

        for _ in range(30):  # iteraciones de escape
            zx2 = zx * zx - zy * zy + c_re
            zy2 = 2 * zx * zy + c_im
            zx, zy = zx2, zy2

            if zx*zx + zy*zy > 4:
                xs.append(x)
                ys.append(y)
                break

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=0.1, color="black")
    plt.title("Julia Set")
    plt.axis("equal")
    plt.show()

def safe_float(x):
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return x