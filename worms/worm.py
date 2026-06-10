import pygame
import random
import math

# =========================
# CONFIGURACIÓN DEL SISTEMA
# =========================
WIDTH = 800
HEIGHT = 800
CELL_SIZE = 5

NUM_WORMS = 20
NUM_FOOD = 80

INITIAL_ENERGY = 100
ENERGY_DECAY = 0.2
ENERGY_GAIN = 40

REPRODUCTION_THRESHOLD = 180
REPRODUCTION_COST = 80

VISION_RADIUS = 20

# =========================
# ENTIDADES
# =========================

class Worm:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.energy = INITIAL_ENERGY
        self.direction = random.uniform(0, 2 * math.pi)
        self.alive = True

    def update(self, food_list):
        if not self.alive:
            return None

        # pérdida de energía constante
        self.energy -= ENERGY_DECAY

        if self.energy <= 0:
            self.alive = False
            return None

        # buscar comida cercana
        target = self.find_food(food_list)

        if target:
            self.move_towards(target)
        else:
            self.wander()

        # comer si está cerca
        for food in food_list:
            if self.distance(food) < 6:
                food_list.remove(food)
                self.energy += ENERGY_GAIN

        # reproducción
        if self.energy > REPRODUCTION_THRESHOLD:
            self.energy -= REPRODUCTION_COST
            return Worm(self.x + random.randint(-10, 10),
                        self.y + random.randint(-10, 10))

        return None

    def wander(self):
        self.direction += random.uniform(-0.5, 0.5)
        self.move()

    def move_towards(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        self.direction = math.atan2(dy, dx)
        self.move()

    def move(self):
        self.x += math.cos(self.direction) * 2
        self.y += math.sin(self.direction) * 2

        # límites del mundo
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def find_food(self, food_list):
        closest = None
        closest_dist = float("inf")

        for food in food_list:
            d = self.distance(food)
            if d < VISION_RADIUS and d < closest_dist:
                closest = food
                closest_dist = d

        return closest

    def distance(self, food):
        return math.hypot(self.x - food[0], self.y - food[1])


# =========================
# UTILIDADES
# =========================

def spawn_food():
    return [(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            for _ in range(NUM_FOOD)]


# =========================
# MAIN LOOP
# =========================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Worm Engine V1")

    worms = [Worm() for _ in range(NUM_WORMS)]
    food = spawn_food()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # comida
        for f in food:
            pygame.draw.circle(screen, (0, 255, 0), f, 3)

        # worms
        new_worms = []

        for w in worms:
            baby = w.update(food)
            if baby:
                new_worms.append(baby)

            if w.alive:
                color = (255, 255, 0)
                pygame.draw.circle(screen, color, (int(w.x), int(w.y)), 3)

        worms.extend(new_worms)

        # respawn comida si baja demasiado
        if len(food) < NUM_FOOD // 2:
            food.extend(spawn_food())

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
