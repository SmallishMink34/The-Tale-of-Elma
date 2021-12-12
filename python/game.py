import pygame
import world
import ClassPG


def gaming():

    game = ClassPG.game("Ingame", (1280,720), 60)

    d = {}

    sizemap = 100

    worlde = world.Terrain()

    map = worlde.GenerateTerrain()
    print(map)
    print(len(map))

    tile = pygame.sprite.Group()

    for row in map:
        d[str(row[1])] = world.tiles(f"../img/tile/bloc/tile_{str(row[1])}.png", row[0][0]*8+100,  row[0][1]*8+100)
        tile.add(d[str(row[1])])

    while game.running:
        game.gameloop()

        tile.draw(game.screen)

        game.eventpy()
        
        pygame.display.update()

gaming()