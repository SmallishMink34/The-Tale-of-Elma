import pygame, sys
from pygame.locals import *  # import pygame modules


class Player:
    def __init__(self):
        self.player = pygame.image.load("../img/player/player.png")
        self.rect = self.player.get_rect()  # self.rect.x
        self.moving_left = False
        self.moving_right = False
        self.fall = True
        self.onground = False
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    def blit(self, screen):
        screen.blit(self.player, self.rect)

    def move(self):
        for event in pygame.event.get():  # event loop
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.moving_right = True
                if event.key == K_LEFT:
                    self.moving_left = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.moving_right = False
                if event.key == K_LEFT:
                    self.moving_left = False
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def grav(self):
        if self.fall:
            self.rect.y += 1

    def collision(self, element, tile):
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types
