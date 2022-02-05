import pygame, sys, ClassPG, Gui

from PlayerAnim import AnimateSprite


class Player(pygame.sprite.Sprite):
    """Class créant un joueur sideview"""

    def __init__(self, tile_size, pos: tuple, topdown=True):
        super().__init__()
        self.rigth = False
        self.left = False
        self.name = 'player'
        self.image = pygame.image.load("../img/player/player.png").convert_alpha()
        self.viewleft = True

        self.size_w, self.size_h = tile_size, tile_size * 2

        self.baseimage = pygame.transform.scale(self.image, (tile_size, 2 * tile_size)).convert_alpha()
        self.image = self.baseimage
        self.rect = self.baseimage.get_rect()  # self.rect.x
        self.rect.x, self.rect.y = pos[0], pos[1]

        self.pressed = {}  # Dico qui retient les touche presser
        self.movement = [0, 0]  # Vitesse x et y
        self.air_time = 0
        self.ver = 0

        self.momentum_y = 0  # Vitesse de la chute

        self.fall = False
        self.onground = False
        self.collision_types = None

        self.topdown = topdown

        self.current = 0
        self.zoomscale = 0.40

        self.live = 4
        self.img_live = False

        self.scroll = [0, 0]

        self.run = []
        for i in range(1, 4):
            self.run.append(pygame.image.load(f"img/player/run/{i}.png").convert_alpha())
        print(len(self.run))
        self.idle = []
        for i in range(1, 3):
            self.idle.append(pygame.image.load(f"img/player/idle/{i}.png").convert_alpha())

    def sideview(self):
        if not self.topdown:
            if self.viewleft:
                self.image = self.baseimage
            elif not self.viewleft:
                self.image = pygame.transform.flip(self.baseimage, True, False)

    def dirrection(self):
        self.movement = [0, 0]
        if self.pressed.get(pygame.K_RIGHT):
            self.movement[0] += 2
            self.viewleft = False
        if self.pressed.get(pygame.K_LEFT):
            self.movement[0] -= 2
            self.viewleft = True
        if self.pressed.get(pygame.K_RIGHT) and self.pressed.get(pygame.K_LSHIFT):
            self.movement[0] += 0.5
        if self.pressed.get(pygame.K_LEFT) and self.pressed.get(pygame.K_LSHIFT):
            self.movement[0] -= 0.5
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
                self.rect.right = tile.left
                self.collision_types['right'] = True
            if self.movement[0] < 0:
                self.rect.left = tile.right
                self.collision_types['left'] = True

        self.rect.y += self.movement[1]

        hitlist = self.collision(tiles)
        for tile in hitlist:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                self.collision_types['bottom'] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                self.collision_types['top'] = True

        if not self.collision_types['bottom']:
            self.air_time += 1
        else:
            self.air_time = 0

        self.anim()
        self.sideview()

    def moving(self):
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]

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
            if self.rect.colliderect(tile):
                hit.append(tile)
        return hit

    def anim(self):
        if self.air_time > 5:  # if the player is in air
            self.baseimage = pygame.image.load("img/player/jump/1.png").convert_alpha()
            self.baseimage = pygame.transform.scale(self.baseimage, (self.size_w, self.size_h))
        if self.movement[0] == 0:  # if the character doesn't move
            if self.collision_types['bottom']:
                self.current += 0.1
                if self.current > len(self.idle): self.current = 0
                self.baseimage = pygame.transform.scale(self.idle[int(self.current)],
                                                        (self.size_w, self.size_h)).convert_alpha()
        elif self.movement[0] == 2.5 or self.movement[0] == -2.5:
            if self.collision_types['bottom']:
                self.current += 0.50  # ca vas etre un chiffre qui augmente

                if int(self.current) >= len(self.run): self.current = 0
                self.baseimage = pygame.transform.scale(self.run[int(self.current)],
                                                        (self.size_w, self.size_h)).convert_alpha()
        else:
            if self.collision_types['bottom']:
                self.current += 0.05  # ca vas etre un chiffre qui augmente
                if self.current > len(self.idle): self.current = 0
                self.baseimage = pygame.transform.scale(self.idle[int(self.current)],
                                                        (self.size_w, self.size_h)).convert_alpha()


class PlayerTopDown(AnimateSprite):
    """
    Class créant un joueur TopDown
    """
    def __init__(self, name, spawncoords, screen):
        super(PlayerTopDown, self).__init__()
        self.name = name
        self.tilesize = 16
        self.tilesizescale = 2
        self.screen = screen

        self.type = 'Joueur'
        self.image = self.get_coords_image(0, 0)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()



        self.pressed = {}
        self.speed = 3
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        self.old_position = spawncoords

        self.move(spawncoords[0], spawncoords[1])

        self.KeyAction = True
        self.canPressKey = True

        self.gui = Gui.Gui('Normal', self)

    def update(self):
        self.save_old_location()  # Savegarde des position du joueur avant mouvement
        self.dirrection()  # Deplacement joueur
        self.KeyAction = False

        if self.pressed.get(pygame.K_e):
            pass

    def get_coords_image(self, x, y):
        """
        Recuperer l'image sur une tile sheet
        :param x: int
        :param y: int
        :return: Surface
        """
        image = pygame.Surface([self.tilesize * self.tilesizescale, self.tilesize * self.tilesizescale]).convert_alpha()
        image = pygame.transform.scale(image, (self.tilesize * self.tilesizescale, self.tilesize * self.tilesizescale))
        image.blit(self.sprite, (0, 0), (x, y, self.tilesize * self.tilesizescale, self.tilesize * self.tilesizescale))
        return image

    def dirrection(self):
        """
        Dirrige le joueur dans une dirrection
        :return: Nothing
        """
        if self.canPressKey:
            if self.pressed.get(pygame.K_d):
                self.move(self.rect.x + self.speed, self.rect.y)
                self.animation('right')
            if self.pressed.get(pygame.K_q):
                self.move(self.rect.x - self.speed, self.rect.y)
                self.animation('left')
            if self.pressed.get(pygame.K_z):
                self.move(self.rect.x, self.rect.y - self.speed)
                self.animation('up')
            if self.pressed.get(pygame.K_s):
                self.move(self.rect.x, self.rect.y + self.speed)
                self.animation('down')

    def move(self, x, y):
        """
        Update les coordonées du joueurs et de ses pieds
        :param x: int
        :param y: int
        :return: Nothing
        """
        self.rect.x = x
        self.rect.y = y

        self.feet.midbottom = self.rect.midbottom



    def save_old_location(self):
        """
        Recuperer l'ancienne position du joueur
        :return: Nothing
        """
        self.old_position = (self.rect.x, self.rect.y)

    def moveback(self):
        """
        Teleporte le joueur aux anciennes coordonées
        :return: Nothing
        """
        self.rect.x, self.rect.y = self.old_position[0], self.old_position[1]
        self.feet.midbottom = self.rect.midbottom
        self.animation_i = 0

    def inputaction(self):
        """ Fait apparaitre la touche d'action et permet son utilisation
        :return: Nothing
        """
        if self.canPressKey:
            self.KeyAction = True
            if self.pressed.get(pygame.K_e):
                self.pressed[pygame.K_e] = False
                return True

    def allinputoff(self, switch=None):
        """
        Desactive/Active les touches de déplacement
        :param switch: Boolean
        :return: Nothing
        """
        if switch is None:
            if self.canPressKey:
                self.canPressKey = False
            else:
                self.canPressKey = True
        else:
            self.canPressKey = switch
