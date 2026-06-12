import math
import random


# =========================
# UTILIDADES SEGURIDAD NUMÉRICA
# =========================
def safe(x):
    """Evita NaN e inf que rompen JSON y WebSockets."""
    if x is None:
        return 0.0
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return 0.0
    return x


# =========================
# HENON MAP
# =========================
def henon(x, y, a=1.4, b=0.3):
    """
    Sistema de Hénon:
    x' = 1 - a x^2 + y
    y' = b x
    """
    nx = 1 - a * x * x + y
    ny = b * x
    return safe(nx), safe(ny)


# =========================
# LORENZ FIELD (proyección 2D simplificada)
# =========================
def lorenz(x, y, z=0.0, sigma=10.0, rho=28.0, beta=8.0/3.0, dt=0.01):
    """
    Lorenz simplificado proyectado a 2D.
    """
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    x += dx * dt
    y += dy * dt
    z += dz * dt

    return safe(x), safe(y)


# =========================
# RÖSSLER FIELD (proyección 2D)
# =========================
def rossler(x, y, z=0.0, a=0.2, b=0.2, c=5.7, dt=0.01):
    dx = -y - z
    dy = x + a * y
    dz = b + z * (x - c)

    x += dx * dt
    y += dy * dt
    z += dz * dt

    return safe(x), safe(y)


# =========================
# JULIA FIELD (tipo potencial caótico)
# =========================
def julia_field(x, y, cx=-0.7, cy=0.27015, max_iter=8):
    """
    Campo tipo Julia para fuerzas visuales.
    No es fractal puro, es versión "force field".
    """
    zx, zy = x, y

    for _ in range(max_iter):
        zx2 = zx * zx - zy * zy + cx
        zy2 = 2 * zx * zy + cy
        zx, zy = zx2, zy2

        if zx * zx + zy * zy > 4:
            break

    return safe(zx), safe(zy)


# =========================
# CAMPO MIXTO (CLAVE V3)
# =========================
def mixed_field(x, y, params):
    """
    Mezcla dinámica de sistemas.
    params:
        {
            "henon": 0.5,
            "lorenz": 0.3,
            "rossler": 0.2
        }
    """

    hx, hy = henon(x, y)
    lx, ly = lorenz(x, y)
    rx, ry = rossler(x, y)

    w_h = params.get("henon", 0.0)
    w_l = params.get("lorenz", 0.0)
    w_r = params.get("rossler", 0.0)

    fx = (hx * w_h + lx * w_l + rx * w_r)
    fy = (hy * w_h + ly * w_l + ry * w_r)

    return safe(fx), safe(fy)


# =========================
# CAMPO PRINCIPAL
# =========================
def compute_field(x, y, system="henon", params=None):
    """
    API unificada del sistema.
    """
    if params is None:
        params = {}

    if system == "henon":
        return henon(x, y,
                     a=params.get("a", 1.4),
                     b=params.get("b", 0.3))

    if system == "lorenz":
        return lorenz(x, y)

    if system == "rossler":
        return rossler(x, y)

    if system == "julia":
        return julia_field(x, y)

    if system == "mixed":
        return mixed_field(x, y, params)

    # fallback seguro
    return safe(math.sin(x)), safe(math.cos(y))