import random
import math

from core.fields import compute_field


class ChaosEngine:
    def __init__(self, n_agents=300):

        self.n_agents = n_agents

        self.system = "henon"
        self.params = {
            "a": 1.4,
            "b": 0.3,
        }

        # mundo
        self.bounds = 1.0  # espacio [-1,1]
        self.damping = 0.97
        self.speed = 0.005
        self.noise = 0.01

        # worms
        self.MAX_TRAIL = 3
        self.trail_decay = True

        # interacción social
        self.interaction_radius = 0.15
        self.repulsion_strength = 0.02
        self.attraction_strength = 0.005

        # atractor global móvil
        self.attractor = [random.uniform(-1, 1), random.uniform(-1, 1)]

        self.agents = []
        self.reset()

    # -------------------------
    # RESET
    # -------------------------
    def reset(self, n_agents=None):
        if n_agents:
            self.n_agents = n_agents

        self.agents = []

        for _ in range(self.n_agents):
            self.agents.append({
                "x": random.uniform(-1, 1),
                "y": random.uniform(-1, 1),
                "vx": random.uniform(-0.01, 0.01),
                "vy": random.uniform(-0.01, 0.01),
                "trail": []
            })

    # -------------------------
    # FIELD
    # -------------------------
    def _field(self, x, y):
        fx, fy = compute_field(
            x, y,
            system=self.system,
            params=self.params
        )

        fx += random.uniform(-self.noise, self.noise)
        fy += random.uniform(-self.noise, self.noise)

        return fx, fy

    # -------------------------
    # SOCIAL INTERACTION
    # -------------------------
    def _social_force(self, a):
        fx, fy = 0.0, 0.0

        for b in self.agents:
            if a is b:
                continue

            dx = b["x"] - a["x"]
            dy = b["y"] - a["y"]

            dist2 = dx*dx + dy*dy

            if dist2 < 1e-6 or dist2 > self.interaction_radius**2:
                continue

            dist = math.sqrt(dist2)

            # repulsión fuerte muy cerca
            if dist < 0.03:
                fx -= dx * self.repulsion_strength
                fy -= dy * self.repulsion_strength

            # atracción suave
            fx += dx * self.attraction_strength
            fy += dy * self.attraction_strength

        return fx, fy

    # -------------------------
    # ATTRACTOR
    # -------------------------
    def _attractor_force(self, a):
        dx = self.attractor[0] - a["x"]
        dy = self.attractor[1] - a["y"]

        return dx * 0.01, dy * 0.01

    # -------------------------
    # STEP AGENT
    # -------------------------
    def _step_agent(self, a):

        x, y = a["x"], a["y"]

        fx, fy = self._field(x, y)

        sx, sy = self._social_force(a)
        ax, ay = self._attractor_force(a)

        # dinámica total
        a["vx"] += (fx + sx + ax) * self.speed
        a["vy"] += (fy + sy + ay) * self.speed

        a["vx"] *= self.damping
        a["vy"] *= self.damping

        a["x"] += a["vx"]
        a["y"] += a["vy"]

        # 🌍 TOROIDE B (wrap + reset worm)
        wrapped = False

        if a["x"] > self.bounds:
            a["x"] = -self.bounds
            wrapped = True
        elif a["x"] < -self.bounds:
            a["x"] = self.bounds
            wrapped = True

        if a["y"] > self.bounds:
            a["y"] = -self.bounds
            wrapped = True
        elif a["y"] < -self.bounds:
            a["y"] = self.bounds
            wrapped = True

        if wrapped:
            a["trail"] = []  # clave estética worms

        # safe
        a["vx"] = self._safe(a["vx"])
        a["vy"] = self._safe(a["vy"])

        # trail update
        a["trail"].insert(0, (a["x"], a["y"]))

        if len(a["trail"]) > self.MAX_TRAIL:
            a["trail"].pop()

    # -------------------------
    # SAFE
    # -------------------------
    def _safe(self, v):
        if math.isnan(v) or math.isinf(v):
            return 0.0

        return max(-5, min(5, v))

    # -------------------------
    # STEP WORLD
    # -------------------------
    def step(self):
        for a in self.agents:
            self._step_agent(a)

        # mover atractor lentamente
        self.attractor[0] += random.uniform(-0.005, 0.005)
        self.attractor[1] += random.uniform(-0.005, 0.005)

        return self.get_state()

    # -------------------------
    # STATE
    # -------------------------
    def get_state(self):
        return {
            "system": self.system,
            "params": self.params,
            "attractor": self.attractor,
            "agents": [
                {
                    "pos": (a["x"], a["y"]),
                    "trail": a["trail"]
                }
                for a in self.agents
            ]
        }

    # -------------------------
    # CONTROL
    # -------------------------
    def set_system(self, system):
        self.system = system

    def update_params(self, params):
        self.params.update(params)

    def set_damping(self, value):
        self.damping = float(value)

    def set_speed(self, value):
        self.speed = float(value)

    def set_noise(self, value):
        self.noise = float(value)