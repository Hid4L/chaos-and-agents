import random

def create_agent():
    return {
        "x": random.uniform(-1, 1),
        "y": random.uniform(-1, 1),
        "vx": 0.0,
        "vy": 0.0,
        "energy": random.uniform(0.5, 1.0),
        "age": 0
    }

def clamp(v, min_v=-10, max_v=10):
    return max(min_v, min(max_v, v))

def step_agent(a, fx, fy):
    # influencia del campo
    a["vx"] += fx * 0.01
    a["vy"] += fy * 0.01

    # amortiguación
    a["vx"] *= 0.98
    a["vy"] *= 0.98

    # movimiento
    a["x"] += a["vx"]
    a["y"] += a["vy"]

    # vida
    a["energy"] -= 0.001
    a["age"] += 1

    a["x"] = clamp(a["x"])
    a["y"] = clamp(a["y"])
    a["vx"] = clamp(a["vx"], -1, 1)
    a["vy"] = clamp(a["vy"], -1, 1)
