import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(AnimateSprite, self).__init__()

        self.tilesize = 16
        self.tilesizescale = 2

        self.animation_i = 0
        self.max_img = 4

        self.sprite = pygame.image.load("../img/PlayerTopDown/Player.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (
            self.sprite.get_size()[0] * self.tilesizescale, self.sprite.get_size()[1] * self.tilesizescale))

        self.moveimage = {
            'down': self.get_images(128),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96),
        }

        self.speed = 2
        self.clock = 0

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

    def get_images(self, y):
        images = []
        for i in range(0, self.max_img):
            x = i * self.tilesize * self.tilesizescale
            image = self.get_coords_image(x, y)
            images.append(image)
        return images

    def animation(self, name):
        """
        Dirrige l'image du joueur en fonction de la dirrection
        :param name: str
        :return: Nothing
        """
        self.image = self.moveimage[name][int(self.animation_i)]
        self.image.set_colorkey((0, 0, 0))

        self.clock += self.speed * 8
        if self.clock >= 100:
            self.animation_i += 1
            if self.animation_i >= self.max_img:
                self.animation_i = 0

            self.clock = 0