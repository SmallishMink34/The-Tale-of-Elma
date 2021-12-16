import pygame
import sys
import world
import ClassPG
import ClassPlayer
from pygame.locals import *
import Camera

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

world = Camera.World(pygame.Rect(0,0,1280,720), game.screen, [cp])
camera = Camera.GameCamera((1280, 720), world, (0,0))
camera.turn_on()
camera.zoom()
camera.track(cp.rect)
while game.running:  # game

    display.fill((135, 206, 235))

    game.gameloop()

    tile.draw(display)





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
    if cp.cond:
        if cp.current < 1:
            cp.anim()
        else:
            cp.current = 0
    if cp.movement[0] > 0:
        display.blit(pygame.transform.flip(cp.player, True, False), cp.rect)
        cp.left = True
        cp.rigth = False
    if cp.movement[0] < 0:
        cp.left = False
        cp.rigth = True
        display.blit(cp.player, cp.rect)
    if cp.movement[0] == 0:
        if cp.left:
            display.blit(pygame.transform.flip(cp.player, True, False), cp.rect)
        else:
            display.blit(cp.player, cp.rect)
    game.screen.blit(pygame.transform.scale(display, (1280, 720)), (0, 0))
    
    ##################################### Update de la fenetre ##########################################"
    camera.display(game.screen)
    pygame.display.update()
