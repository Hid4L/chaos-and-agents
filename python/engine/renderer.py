import pygame

class Renderer:
    def __init__(self, world):
        self.world = world
        self.screen = pygame.display.set_mode(
            (world.width, world.height)
        )

    def clear(self):
        self.screen.fill((0, 0, 0))

    def present(self):
        pygame.display.flip()

    def draw_world(self):
        self.world.draw(self.screen)