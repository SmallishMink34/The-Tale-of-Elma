import pygame
import ClassPG
import ClassPlayer
import map
import inv
import fight
from valeurs import *


class Game():
    """
    Class du jeux
    """
    def __init__(self, size=(1280,720, False)):
        self.display_w, self.display_h = size[0], size[1]

        self.game = ClassPG.game("Ingame", (self.display_w, self.display_h), 60, size[2])

        self.display = pygame.Surface((self.display_w, self.display_h))

        self.player = ClassPlayer.PlayerTopDown(valeur.name,(0, 0), self.display)

        self.map_manag = map.Mapmanager(self.display, self.player)

        self.nuit = PG.img("../img/transition/fade/Fade_00000.png", 0, 0, self.display_w, self.display_h, False)


    def run(self):
        """
        Mise en marche du jeux
        :return: Nothing
        """
        running = True
        clock = pygame.time.Clock()

        while running:

            self.game.screen.blit(self.display, (0, 0))
            self.map_manag.updating() # Met a jour la carte et le joueur
            self.map_manag.draw() # Dessine la carte

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    self.player.pressed[event.key] = True
                if event.type == pygame.KEYUP:
                    self.player.pressed[event.key] = False
                self.player.gui.event((x, y), event)

                if self.player.pressed.get(valeur.l["inventory"]):
                    self.player.gui.inventory(self.player.inventaire)
                    self.player.pressed[valeur.l["inventory"]] = False
                if self.player.pressed.get(pygame.K_o):
                    self.map_manag.reload_maps()
                    break

            self.player.gui.iblit(self.display)

            clock.tick(60)
            pygame.display.update()
        pygame.quit()

"""gamee = Game()
gamee.run()"""