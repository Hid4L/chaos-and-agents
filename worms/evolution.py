import random
import copy
from engine import Worm, Config


# =========================
# ADN BASE
# =========================
class DNA:
    def __init__(self):
        self.speed = random.uniform(0.8, 2.0)
        self.vision = random.uniform(80, 250)
        self.metabolism = random.uniform(0.1, 0.4)

    def mutate(self):
        if random.random() < 0.3:
            self.speed += random.uniform(-0.2, 0.2)

        if random.random() < 0.3:
            self.vision += random.uniform(-20, 20)

        if random.random() < 0.3:
            self.metabolism += random.uniform(-0.05, 0.05)

        # clamp
        self.speed = max(0.2, min(3.0, self.speed))
        self.vision = max(50, min(400, self.vision))
        self.metabolism = max(0.05, min(1.0, self.metabolism))


# =========================
# WORM EVOLUTIVO
# =========================
class EvoWorm(Worm):
    def __init__(self, x, y, config, dna=None):
        super().__init__(x, y, config)
        self.dna = dna if dna else DNA()

    def update(self, food_list):
        if not self.alive:
            return

        # metabolismo dinámico (clave evolución)
        self.energy -= self.config.ENERGY_LOSS * self.dna.metabolism

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
        self.direction += random.uniform(-0.5, 0.5)
        self.x += random.uniform(-1, 1) * self.dna.speed
        self.y += random.uniform(-1, 1) * self.dna.speed
        self.wrap()

    def move_towards(self, tx, ty):
        import math
        angle = math.atan2(ty - self.y, tx - self.x)
        self.x += math.cos(angle) * self.dna.speed * 1.5
        self.y += math.sin(angle) * self.dna.speed * 1.5
        self.wrap()

    def reproduce(self):
        if self.energy > 120:
            child_dna = copy.deepcopy(self.dna)
            child_dna.mutate()

            child = EvoWorm(
                self.x + random.randint(-5, 5),
                self.y + random.randint(-5, 5),
                self.config,
                child_dna
            )

            self.energy *= 0.5
            return child

        return None
