import pygame
import sys
import world
import ClassPG
import ClassPlayer
from pygame.locals import *

clock = pygame.time.Clock()
game = ClassPG.game("Ingame", (1280, 720), 60)
display = pygame.Surface((1280, 720))
cp = ClassPlayer.Player()
d = {}
worlde = world.Terrain()
map = worlde.GenerateTerrain()
tile = pygame.sprite.Group()
tile_size = 16
for column in map:
    for row in column:
        d[str(row[1])] = world.tiles(str(row[1]), f"../img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png",
                                     row[0][0] * tile_size, row[0][1] * tile_size + 800, tile_size)

        tile.add(d[str(row[1])])



while game.running:  # game

    display.fill((135,206,235))

    game.gameloop()

    tile.draw(display)

    display.blit(cp.player, cp.rect)

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            cp.pressed[event.key] = True
        if event.type == KEYUP:
            cp.pressed[event.key] = False

    cp.dirrection()
    cp.move(tile)
    cp.jump()

    game.screen.blit(pygame.transform.scale(display, (1280, 720)), (0, 0))
    pygame.display.update()
