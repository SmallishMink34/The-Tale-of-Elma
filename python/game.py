import pygame
import sys
import world
import ClassPG
import ClassPlayer
from pygame.locals import *
import Camera

def gaming():
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
    game = ClassPG.game("Ingame", (display_w,display_h), 60)

    d = {}

    tile_size = 8
    sizemap = 100

    worlde = world.Terrain()

    map = worlde.GenerateTerrain()
    print(map)
    print(len(map))

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

        # for i in tile:
        #     i.set_coord(i.rect.x + cp.scroll[0]/5, i.rect.y - cp.scroll[1])
        cp.zoomscale = 0.5
        camera = Camera.GameCamera([display_w*cp.zoomscale, display_h*cp.zoomscale], world, (0,0))
        camera.zoom(1/cp.zoomscale)
        camera.track(cp.rect)
        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre

            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                sys.exit()
            x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                cp.pressed[event.key] = True
            if event.type == KEYUP:
                cp.pressed[event.key] = False

            '''if event.type == MOUSEBUTTONDOWN:
                cp.zoomscale = 0.5
                camera = Camera.GameCamera([display_w*cp.zoomscale, display_h*cp.zoomscale], world, (0,0))
                camera.zoom(1/cp.zoomscale)
                camera.track(cp.rect)'''
            for i in tile:
                if i.rect.collidepoint(x, y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        worlde.ReplaceTile(i.posinworld[0], i.posinworld[1], 'stone', True)
                        tile = modifymap(worlde.map, tile, i.posinworld[0], i.posinworld[1])

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

gaming()