from engine.fields import field
from engine.agents import step_agent

def step(world):
    system = world["system"]
    t = world["t"]

    for a in world["agents"]:
        fx, fy = field(system, a["x"], a["y"], t)
        step_agent(a, fx, fy)

    world["t"] += 1

    return world