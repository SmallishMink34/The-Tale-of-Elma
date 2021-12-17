import pygame
import world
import ClassPG
import ClassPlayer
from pygame.locals import *  # import pygame modules


def gaming():
    cp = ClassPlayer.Player()
    game = ClassPG.game("Ingame", (1280, 720), 60)

    d = {}

    worlde = world.Terrain()
    map = worlde.GenerateTerrain()
    tile = pygame.sprite.Group()

    for row in map:
        d[str(row[1])] = world.tiles(f"../img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png", row[0][0] * 16 + 10,
                                     row[0][1] * 16 + 500)
        tile.add(d[str(row[1])])

    while game.running:
        game.screen.fill((146, 244, 255))
        cp.blit(game.screen)

        game.gameloop()

        tile.draw(game.screen)

        cp.move()


        cp.grav()

        pygame.display.update()


gaming()
