import matplotlib.pyplot as plt
import math

def run(config):

    n = config.points
    dt = config.dt

    a = config.a
    b = config.b
    c = config.c

    x, y, z = 0.0, 1.0, 0.0

    xs, ys, zs = [], [], []

    for _ in range(n):

        dx = -y - z
        dy = x + a * y
        dz = b + z * (x - c)

        x += dx * dt
        y += dy * dt
        z += dz * dt

        xs.append(x)
        ys.append(y)
        zs.append(z)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(xs, ys, zs, linewidth=0.5, color="blue")
    ax.set_title("Rössler Attractor")

    plt.show()

def safe_float(x):
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return x