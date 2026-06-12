import random
import math


# =========================================================
# 🧠 ENGINE PRINCIPAL
# =========================================================

class ChaosEngine:
    def __init__(self, system="henon", n_agents=200, params=None):
        self.system = system
        self.params = params or {}
        self.agents = []
        self.t = 0

        self.init_agents(n_agents)
        self.growth_rate = 1.0
    # -----------------------------------------------------
    # 🐛 AGENTES
    # -----------------------------------------------------
    def init_agents(self, n):
        self.agents = []
        for _ in range(n):
            self.agents.append({
                "x": random.uniform(-1, 1),
                "y": random.uniform(-1, 1),
                "vx": random.uniform(-0.01, 0.01),
                "vy": random.uniform(-0.01, 0.01),
                "memory": 0.0,   # 🔥 base V3
            })

    # -----------------------------------------------------
    # 🌌 CAMPO CAÓTICO
    # -----------------------------------------------------
    def field(self, x, y):
        if self.system == "henon":
            a = self.params.get("a", 1.4)
            b = self.params.get("b", 0.3)
            return 1 - a * x * x + y + b * x

        elif self.system == "lorenz_like":
            return math.sin(x * 2) * math.cos(y * 2)

        elif self.system == "rossler_like":
            return math.sin(y - x)

        elif self.system == "julia_like":
            return math.cos(x * x + y * y)

        return math.sin(x) * math.cos(y)

    # -----------------------------------------------------
    # 🔒 UTILIDADES DE ESTABILIDAD
    # -----------------------------------------------------
    def clamp(self, v, min_v=-2.0, max_v=2.0):
        return max(min_v, min(max_v, v))

    def clean(self, x):
        if isinstance(x, float):
            if math.isnan(x) or math.isinf(x):
                return 0.0
        return x

    # -----------------------------------------------------
    # 🧬 DINÁMICA AGENTE (BASE V3 READY)
    # -----------------------------------------------------
    def step_agent(self, a):
        fx = self.field(a["x"], a["y"])
        fy = self.field(a["y"], a["x"])

        # 🔥 interacción campo
        a["vx"] += fx * 0.005
        a["vy"] += fy * 0.005

        # 🧊 amortiguación energética
        a["vx"] *= 0.95
        a["vy"] *= 0.95

        # movimiento
        a["x"] += a["vx"]
        a["y"] += a["vy"]

        # 🔒 estabilidad
        a["x"] = self.clamp(a["x"])
        a["y"] = self.clamp(a["y"])

        # 🧠 memoria (base para V3)
        a["memory"] = 0.9 * a["memory"] + 0.1 * (abs(fx) + abs(fy))

    # -----------------------------------------------------
    # 🔁 STEP GLOBAL
    # -----------------------------------------------------
    def step(self):
        self.t += 1

        for a in self.agents:
            self.step_agent(a)

        return {
            "t": self.t,
            "agents": [
                {
                    "x": self.clean(a["x"]),
                    "y": self.clean(a["y"]),
                    "m": self.clean(a["memory"])
                }
                for a in self.agents
            ]
        }

    # -----------------------------------------------------
    # 🔄 RESET
    # -----------------------------------------------------
    def reset(self, n=None):
        if n:
            self.init_agents(n)
        else:
            self.init_agents(len(self.agents))
        self.t = 0