import pygame
from engine.world import World
from engine.renderer import Renderer
from engine.timer import Timer
from systems.worms import WormSystem

def main():
    pygame.init()

    world = World(800, 600)
    renderer = Renderer(world)
    timer = Timer(60)

    worms = WormSystem(n=20)
    world.add(worms)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update()

        renderer.clear()
        world.draw(renderer.screen)
        renderer.present()

        timer.tick()

    pygame.quit()

if __name__ == "__main__":
    main()