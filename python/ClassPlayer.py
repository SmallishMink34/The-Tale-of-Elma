import pygame, sys



class Player:
    def __init__(self):
        self.player = pygame.image.load("../img/player/player.png").convert_alpha()
        self.rect = self.player.get_rect()  # self.rect.x
        self.rect.x, self.rect.y = 250, 80

        self.pressed = {} # Dico qui retient les touche presser
        self.movement = [0, 0] #Vitesse x et y

        self.momentum_y = 0 # Vitesse de la chute

        self.fall = True
        self.onground = False
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    def blit(self, screen):
        screen.blit(self.player, self.rect)

    def dirrection(self):
        self.movement = [0, 0]
        if self.pressed.get(pygame.K_d):
            self.movement[0] += 2
        if self.pressed.get(pygame.K_q):
            self.movement[0] -= 2
        self.movement[1] += self.momentum_y
        self.momentum_y += 0.2
        if self.momentum_y > 3:
            self.momentum_y = 3


    def move(self, tiles):
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

    def collision(self, tiles):
        hit = []
        for tile in tiles:
            if self.rect.colliderect(tile) and tile.name != 'air':
                hit.append(tile)

        return hit

