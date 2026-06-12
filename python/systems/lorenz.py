import matplotlib.pyplot as plt
import math

def run(config):

    n = config.points
    dt = config.dt

    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    x, y, z = 0.0, 1.0, 1.05

    xs, ys, zs = [], [], []

    for _ in range(n):

        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

        x += dx * dt
        y += dy * dt
        z += dz * dt

        xs.append(x)
        ys.append(y)
        zs.append(z)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(xs, ys, zs, linewidth=0.5)
    ax.set_title("Lorenz Attractor")

    plt.show()

def safe_float(x):
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return x