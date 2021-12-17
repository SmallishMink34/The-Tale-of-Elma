import pygame
import sys
import world
import ClassPG
import ClassPlayer
from pygame.locals import *
import Camera

clock = pygame.time.Clock()
game = ClassPG.game("Ingame", (1280, 720), 60)

display_w, display_h = 1280, 720

display = pygame.Surface((1280, 720))

cp = ClassPlayer.Player()

d = {}
worlde = world.Terrain()

map = worlde.GenerateTerrain()

tile = pygame.sprite.Group()

tile_size = 16
for column in map:
    for row in column:
        d[str(row[1])] = world.tiles(str(row[1]), f"img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png",
                                     row[0][0] * tile_size, row[0][1] * tile_size + 800, tile_size)

        tile.add(d[str(row[1])])

world = Camera.World(pygame.Rect(0,0,1280,720), game.screen, [cp])

# camera = Camera.GameCamera([display_w*cp.zoomscale, display_h*cp.zoomscale], world, (0,0))
# camera.turn_on()
# camera.zoom(1/cp.zoomscale)
# camera.track(cp.rect)

while game.running:  # game
     
    cp.scroll[0] = 1
      
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
        

    # for i in tile:
    #     i.set_coord(i.rect.x + cp.scroll[0]/5, i.rect.y - cp.scroll[1])
    cp.zoomscale = 0.5
    camera = Camera.GameCamera([display_w*cp.zoomscale, display_h*cp.zoomscale], world, (0,0))
    camera.zoom(1/cp.zoomscale)
    camera.track(cp.rect)

    cp.dirrection()
    cp.move(tile)
    cp.jump()
    
    ########################################################################
    ###                          ANIMATION                               ###
    ########################################################################
    if cp.current < 1: 
        cp.anim()
    else:
        cp.current = 0
        
    if cp.movement[0] > 0: # if player => left
        display.blit(pygame.transform.flip(cp.player, True, False), (cp.rect.x + cp.scroll[0], cp.rect.y + cp.scroll[1] ))
        cp.left = True
        cp.rigth = False
    if cp.movement[0] < 0: # if player => right
        cp.left = False
        cp.rigth = True
        display.blit(cp.player, (cp.rect.x + cp.scroll[0] , cp.rect.y + cp.scroll[1]))
    if cp.movement[0] == 0: # if player => none
        if cp.left:
            display.blit(pygame.transform.flip(cp.player, True, False), (cp.rect.x + cp.scroll[0], cp.rect.y + cp.scroll[1]))
        else:
            display.blit(cp.player, (cp.rect.x + cp.scroll[0] , cp.rect.y + cp.scroll[1]))
    game.screen.blit(display, (0, 0))
    
    ##################################### Update de la fenetre ##########################################"
    camera.display(game.screen)
    pygame.display.update()
