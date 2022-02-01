import pygame
import ClassPG
import ClassPlayer
from pygame.locals import *
import sys
import pyscroll
import pytmx


class Game():
    def __init__(self):
        self.display_w, self.display_h = 1280, 720

        self.game = ClassPG.game("Ingame", (self.display_w, self.display_h), 60)

        tmx = pytmx.util_pygame.load_pygame("../img/tile/Lobby.tmx")
        mapdata = pyscroll.data.TiledMapData(tmx)
        map_layer = pyscroll.orthographic.BufferedRenderer(mapdata, (self.display_w//2, self.display_h//2))
        map_layer.zoom = 2


        self.map = []
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        display = pygame.Surface((640, 360))

        while running:
            self.game.screen.fill((255, 25, 48))
            self.game.screen.blit(display, (0, 0))

            self.group.update()


            self.group.draw(display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                x, y = pygame.mouse.get_pos()

            clock.tick(60)
            pygame.display.update()

        pygame.quit()



game = Game()
game.run()
