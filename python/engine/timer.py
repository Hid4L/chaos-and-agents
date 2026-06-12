import pygame

class Timer:
    def __init__(self, fps=60):
        self.clock = pygame.time.Clock()
        self.fps = fps

    def tick(self):
        self.clock.tick(self.fps)