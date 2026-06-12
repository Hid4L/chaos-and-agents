import math
import matplotlib.pyplot as plt


def run(config):

    a = config.a
    b = config.b
    n = config.points

    x, y = 0.0, 0.0
    xs, ys = [], []

    for _ in range(n):
        x_new = 1 - a * x * x + y
        y_new = b * x

        x, y = x_new, y_new

        xs.append(x)
        ys.append(y)

    plt.scatter(xs, ys, s=0.1)
    plt.title("Henon Attractor")
    plt.show()

def safe_float(x):
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return x