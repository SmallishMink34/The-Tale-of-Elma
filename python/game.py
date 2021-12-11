import pygame
import world
import ClassPG


def gaming():

    game = ClassPG.game("Ingame", (1280,720), 60)

    d = {}
    for i in range(1, 4):
        d[i] = world.tiles(f"img/tile/bloc/tile_{i}.png")
    
    map = []
    for i2 in range(3):
        print(map)
        for i3 in range(3):
            map += world.generate_chunk(i2, i3)
    print(map[1])
    while game.running:
        game.gameloop()

        for row in map:
            d[row[1]].setcoord(row[0][0]*48,row[0][1]*48)
            d[row[1]].iblit(game.screen)

        game.eventpy()

        
        pygame.display.update()

gaming()