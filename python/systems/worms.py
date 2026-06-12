import random
import pygame
import math

class Worm:
    def __init__(self, x, y, length=10):
        self.body = [(x, y)]
        self.length = length
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, world):
        # movimiento tipo random walk controlado
        self.angle += random.uniform(-0.3, 0.3)

        head_x, head_y = self.body[0]

        new_x = head_x + math.cos(self.angle) * 2
        new_y = head_y + math.sin(self.angle) * 2

        self.body.insert(0, (new_x, new_y))

        if len(self.body) > self.length:
            self.body.pop()

        # rebote en bordes
        if new_x < 0 or new_x > world.width:
            self.angle += math.pi
        if new_y < 0 or new_y > world.height:
            self.angle += math.pi

    def draw(self, screen):
        for p in self.body:
            pygame.draw.circle(screen, (255, 255, 255), (int(p[0]), int(p[1])), 2)


class WormSystem:
    def __init__(self, n=10, width=800, height=600):
        self.worms = [
            Worm(
                random.randint(0, width),
                random.randint(0, height)
            )
            for _ in range(n)
        ]

    def update(self, world):
        for w in self.worms:
            w.update(world)

    def draw(self, screen):
        for w in self.worms:
            w.draw(screen)