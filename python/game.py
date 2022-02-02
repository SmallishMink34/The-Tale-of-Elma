import pygame
import ClassPG
import ClassPlayer
from pygame.locals import *
import sys
import pyscroll
import pytmx
import map

class Game():
    """
    Class du jeux
    """
    def __init__(self):
        self.display_w, self.display_h = 1280, 720

        self.game = ClassPG.game("Ingame", (self.display_w, self.display_h), 60)

        self.player = ClassPlayer.PlayerTopDown((0, 0))

        self.map_manag = map.Mapmanager(self.game.screen, self.player)

    def run(self):
        """
        Mise en marche du jeux
        :return: Nothing
        """
        running = True
        clock = pygame.time.Clock()
        display = pygame.Surface((self.display_w, self.display_h))

        while running:
            self.game.screen.fill((255, 25, 48))
            self.game.screen.blit(display, (0, 0))

            self.player.save_old_location()  # Savegarde des position du joueur avant mouvement

            self.player.dirrection()  # Deplacement joueur

            self.map_manag.updating() # Met a jour la carte et le joueur
            self.map_manag.draw()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    self.player.pressed[event.key] = True
                if event.type == pygame.KEYUP:
                    self.player.pressed[event.key] = False


            clock.tick(60)
            pygame.display.update()

        pygame.quit()



game = Game()
game.run()
