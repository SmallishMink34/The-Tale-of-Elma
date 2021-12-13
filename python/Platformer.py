import pygame
import sys
import world
import ClassPG
import ClassPlayer
from pygame.locals import *

clock = pygame.time.Clock()

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        print("test")
        if rect.colliderect(d[tile[0][1]].rect):
            hit_list.append(d[tile[0][1]].rect)
    return hit_list
def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


cp = ClassPlayer.Player()
game = ClassPG.game("Ingame", (1280, 720), 60)

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

d = {}
worlde = world.Terrain()
map = worlde.GenerateTerrain()
tileee = pygame.sprite.Group()
tile_size = 8
for column in map:
    for row in column:
        d[str(row[1])] = world.tiles(str(row[1]), f"../img/tile/bloc/PNG/Tiles/tile_{str(row[1])}.png",
                                     row[0][0] * tile_size, row[0][1] * tile_size + 500, tile_size)

        tileee.add(d[str(row[1])])


true_scroll = [0,0]



game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')

player_img = pygame.image.load('../img/player/player.png').convert()
player_img.set_colorkey((255,255,255))

player_rect = pygame.Rect(100,100,5,13)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]



while game.running: # game loop

    game.screen.fill((146, 244, 255))

    game.gameloop()

    tileee.draw(game.screen)


    pygame.draw.rect(game.screen,(7,50,75),pygame.Rect(0,120,300,80))


    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                game.screen.blit(dirt_img,(x*16,y*16))
            if tile == '2':
                game.screen.blit(grass_img,(x*16,y*16))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    player_rect,collisions = move(player_rect,player_movement,map)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    game.screen.blit(player_img,(player_rect.x,player_rect.y))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    pygame.display.update()
