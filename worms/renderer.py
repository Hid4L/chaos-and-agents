import pygame
from engine import Engine, Config

# =========================
# INIT
# =========================
pygame.init()

WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Worm Engine v1")

clock = pygame.time.Clock()

engine = Engine(Config)

# =========================
# LOOP
# =========================
running = True

while running:
    clock.tick(60)
    screen.fill((15, 15, 20))

    # eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # avanzar simulación
    engine.step()

    state = engine.get_state()

    # =========================
    # DRAW FOOD
    # =========================
    for fx, fy in state["food"]:
        pygame.draw.circle(screen, (255, 200, 0), (int(fx), int(fy)), 3)

    # =========================
    # DRAW WORMS
    # =========================
    for w in state["worms"]:
        x = int(w["x"])
        y = int(w["y"])

        if w["alive"]:
            # color según energía
            energy_ratio = w["energy"] / Config.MAX_ENERGY
            green = int(200 * energy_ratio)
            color = (50, green, 80)
        else:
            color = (60, 60, 60)

        pygame.draw.circle(screen, color, (x, y), 4)

        # barra de energía
        pygame.draw.rect(
            screen,
            (200, 50, 50),
            pygame.Rect(x - 10, y - 10, 20, 3)
        )
        pygame.draw.rect(
            screen,
            (50, 220, 50),
            pygame.Rect(x - 10, y - 10, int(20 * (w["energy"] / Config.MAX_ENERGY)), 3)
        )

    # info debug
    font = pygame.font.SysFont(None, 20)
    text = font.render(f"Ticks: {state['ticks']}", True, (200, 200, 200))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
