import pygame
import world
import ClassPG
import sys


def gaming():

    game = ClassPG.game("Ingame", (1280,720), 60)

    d = {}

    tile_size = 8
    sizemap = 100

    worlde = world.Terrain()

    map = worlde.GenerateTerrain()

    print(map)
    tile = pygame.sprite.Group()

    for column in map:
        for row in column:
            d[str(row[1])] = world.tiles(str(row[1]),f"../img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png", row[0][0]*tile_size,  row[0][1]*tile_size + 500, tile_size)

            tile.add(d[str(row[1])])

    while game.running:
        game.gameloop()

        tile.draw(game.screen)

        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre

            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                sys.exit()
            x, y = pygame.mouse.get_pos()
            for i in tile:
                if i.rect.collidepoint(x, y):
                    print(i)
        pygame.display.update()
gaming()
