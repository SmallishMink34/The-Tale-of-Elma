import pygame
import world
import ClassPG


def gaming():

    game = ClassPG.game("Ingame", (1280,720), 60)

    d = {}

    map = []
    sizemap = 100
    for i2 in range(sizemap):
        for i3 in range(sizemap):
            pass

    map += world.Genlist(sizemap, sizemap, False)

    print(len(map))

    tile = pygame.sprite.Group()

    for row in map:
        d[str(row[1])] = world.tiles(f"../img/tile/bloc/tile_{str(row[1])}.png", row[0][0]*16,  row[0][1]*16)
        tile.add(d[str(row[1])])

    while game.running:
        game.gameloop()

        tile.draw(game.screen)

        game.eventpy()
        
        pygame.display.update()

gaming()