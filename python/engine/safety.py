import math

MAX_VALUE = 1000


def is_valid(x):
    return not (math.isinf(x) or math.isnan(x))


def safe_float(x):
    if not is_valid(x):
        return 0.0
    return x


def clamp(x, min_v=-MAX_VALUE, max_v=MAX_VALUE):
    return max(min_v, min(max_v, x))


def safe_vector(v):
    return {
        "x": clamp(safe_float(v.get("x", 0))),
        "y": clamp(safe_float(v.get("y", 0))),
    }


def safe_agent(a):
    a["x"] = clamp(safe_float(a["x"]))
    a["y"] = clamp(safe_float(a["y"]))
    a["vx"] = clamp(safe_float(a["vx"]))
    a["vy"] = clamp(safe_float(a["vy"]))
    return a