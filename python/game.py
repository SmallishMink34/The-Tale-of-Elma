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

    tile = pygame.sprite.Group()

    def modifymap(mape,tile,x ,y):
        tiling = tile
        for column in mape:
            for row in column:
                if row[0][0] == x and row[0][1] == -y:
                    for element in tiling:
                        if element.posinworld[0] == x and element.posinworld[1] == -y:
                            element.kill()
                    d[str(row[0])] = world.tiles(str(row[1]), f"../img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png",
                                                 row[0][0] * tile_size, row[0][1] * tile_size + 500,
                                                 [row[0][0], -row[0][1]], tile_size)
                    tiling.add(d[str(row[0])])
                elif x is None and y is None:
                    d[str(row[0])] = world.tiles(str(row[1]), f"../img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png",
                                                 row[0][0] * tile_size, row[0][1] * tile_size + 500,
                                                 [row[0][0], -row[0][1]], tile_size)

                    tiling.add(d[str(row[0])])
        return tiling

    tile = modifymap(map, tile, None, None)


    while game.running:
        game.gameloop()

        tile.draw(game.screen)

        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre

            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                sys.exit()
            x, y = pygame.mouse.get_pos()
            for i in tile:
                if i.rect.collidepoint(x, y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        worlde.ReplaceTile(i.posinworld[0], i.posinworld[1], 'stone', True)
                        tile = modifymap(worlde.map, tile, i.posinworld[0], i.posinworld[1])

        pygame.display.update()
gaming()
