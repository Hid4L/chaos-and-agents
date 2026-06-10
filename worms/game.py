import pygame
import sys

class Game:

    def __init__(self):

      # Configuracion ventana
      self.width = 1000
      self.height = 700

      # Inicializar pygame
      pygame.init()

      self.screen =
  pygame.display.set_mode(
        (self.width, self.height)
  )
      pygame.display.set_caption(
        "Chaos & Agents - Worms V1"
      )

      self.clock = pygame.time.Clock()

      self.running = True

  def handle_events(self):

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              self.running = False

  def update (self):
      """
      Logica del munod
      """"

  def draw(self):

      while self. running:
          self.handle_events()
          self.update()
          self.draw()
          self.clock.tick(60)
        pygame.quit()
        sys.exit()

  def main():
      game = Game()
      game.run()

if __name__ == "__main__"
  main()
