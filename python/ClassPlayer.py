import pygame, sys


class Player:
    def __init__(self):

        self.rigth = False
        self.left = False

        self.player = pygame.image.load("../img/player/player.png")
        self.rect = self.player.get_rect()  # self.rect.x
        self.rect.x, self.rect.y = 250, 80

        self.pressed = {}  # Dico qui retient les touche presser
        self.movement = [0, 0]  # Vitesse x et y
        self.air_time = 0
        self.ver = 0

        self.momentum_y = 0  # Vitesse de la chute

        self.fall = True
        self.onground = False
        self.collision_types = None

        self.current = 0
        self.cond = True

        self.run = []
        for i in range(1, 4):
            self.run.append(pygame.image.load(f"../img/player/run/{i}.png"))

        self.idle = []
        for i in range(1, 3):
            self.idle.append(pygame.image.load(f"../img/player/idle/{i}.png"))

    def dirrection(self):
        self.movement = [0, 0]
        if self.pressed.get(pygame.K_RIGHT):
            self.movement[0] += 2
        if self.pressed.get(pygame.K_LEFT):
            self.movement[0] -= 2
        if self.pressed.get(pygame.K_UP):
            if self.air_time < 6:
                self.momentum_y = -5
        self.movement[1] += self.momentum_y
        self.momentum_y += 0.2
        if self.momentum_y > 3:
            self.momentum_y = 3

    def move(self, tiles):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.movement[0]
        hitlist = self.collision(tiles)
        for tile in hitlist:
            if self.movement[0] > 0:
                self.rect.right = tile.rect.left
                self.collision_types['right'] = True
            if self.movement[0] < 0:
                self.rect.left = tile.rect.right
                self.collision_types['left'] = True

        self.rect.y += self.movement[1]

        hitlist = self.collision(tiles)
        for tile in hitlist:
            if self.movement[1] > 0:
                self.rect.bottom = tile.rect.top
                self.collision_types['bottom'] = True
            if self.movement[1] < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types['top'] = True

    def jump(self):
        if self.collision_types['bottom']:
            self.air_time = 0
            self.momentum_y = 0
        else:
            self.air_time += 1
        if self.collision_types['top']:
            self.momentum_y = 0

    def collision(self, tiles):
        hit = []
        for tile in tiles:
            if self.rect.colliderect(tile) and tile.name != 'air':
                hit.append(tile)
        return hit

    def anim(self):
        print(self.air_time)
        if self.air_time > 5:
            self.player = pygame.image.load("../img/player/jump/1.png")
        if not self.movement[0] == 0:
            if self.collision_types['bottom']:
                self.current += 0.50  # ca vas etre un chiffre qui augmente
                self.player = pygame.transform.scale(self.run[int(self.current)], (16, 32))
        else:
            if self.collision_types['bottom']:
                self.current += 0.05  # ca vas etre un chiffre qui augmente
                self.player = pygame.transform.scale(self.idle[int(self.current)], (16, 32))


