import random
import math


# =========================
# CONFIG
# =========================
class Config:
    WIDTH = 800
    HEIGHT = 800

    NUM_WORMS = 15
    NUM_FOOD = 80

    MAX_ENERGY = 100
    ENERGY_LOSS = 0.2
    ENERGY_GAIN = 35

    MOVE_SPEED = 1.2
    VISION_RANGE = 200


# =========================
# ENTIDADES
# =========================
class Worm:
    def __init__(self, x, y, config):
        self.x = x
        self.y = y
        self.energy = config.MAX_ENERGY
        self.alive = True
        self.config = config
        self.direction = random.uniform(0, 2 * math.pi)

    def update(self, food_list):
        if not self.alive:
            return

        self.energy -= self.config.ENERGY_LOSS
        if self.energy <= 0:
            self.alive = False
            return

        target = self.find_food(food_list)

        if target:
            self.move_towards(target.x, target.y)
        else:
            self.wander()

        self.eat(food_list)

    def wander(self):
        self.direction += random.uniform(-0.4, 0.4)
        self.x += math.cos(self.direction) * self.config.MOVE_SPEED
        self.y += math.sin(self.direction) * self.config.MOVE_SPEED
        self.wrap()

    def move_towards(self, tx, ty):
        angle = math.atan2(ty - self.y, tx - self.x)
        self.x += math.cos(angle) * self.config.MOVE_SPEED * 1.5
        self.y += math.sin(angle) * self.config.MOVE_SPEED * 1.5
        self.wrap()

    def find_food(self, food_list):
        best = None
        best_dist = self.config.VISION_RANGE ** 2

        for f in food_list:
            d = (f.x - self.x) ** 2 + (f.y - self.y) ** 2
            if d < best_dist:
                best_dist = d
                best = f

        return best

    def eat(self, food_list):
        for f in food_list[:]:
            if abs(f.x - self.x) < 6 and abs(f.y - self.y) < 6:
                food_list.remove(f)
                self.energy = min(self.config.MAX_ENERGY,
                                  self.energy + self.config.ENERGY_GAIN)

    def wrap(self):
        self.x %= self.config.WIDTH
        self.y %= self.config.HEIGHT


class Food:
    def __init__(self, config):
        self.x = random.randint(0, config.WIDTH)
        self.y = random.randint(0, config.HEIGHT)


# =========================
# WORLD
# =========================
class World:
    def __init__(self, config):
        self.config = config

        self.worms = [
            Worm(
                random.randint(0, config.WIDTH),
                random.randint(0, config.HEIGHT),
                config
            )
            for _ in range(config.NUM_WORMS)
        ]

        self.food = [
            Food(config)
            for _ in range(config.NUM_FOOD)
        ]

    def update(self):
        # mantener comida
        if len(self.food) < self.config.NUM_FOOD:
            self.food.append(Food(self.config))

        # actualizar gusanos
        for w in self.worms:
            w.update(self.food)


# =========================
# ENGINE
# =========================
class Engine:
    def __init__(self, config=Config):
        self.config = config()
        self.world = World(self.config)
        self.ticks = 0

    def step(self):
        self.world.update()
        self.ticks += 1

    def get_state(self):
        """
        Devuelve estado limpio para render o análisis
        """
        return {
            "worms": [
                {
                    "x": w.x,
                    "y": w.y,
                    "energy": w.energy,
                    "alive": w.alive
                }
                for w in self.world.worms
            ],
            "food": [
                (f.x, f.y) for f in self.world.food
            ],
            "ticks": self.ticks
        }
