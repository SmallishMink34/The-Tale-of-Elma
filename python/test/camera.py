import math
import pygame
from pygame.math import Vector2 as vec


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, walls):
        pygame.sprite.Sprite.__init__(self)
        self.walls = walls
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            pygame.Color('dodgerblue1'),
            ((0, 0), (50, 15), (0, 30)))
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(x, y, 50, 50)
        self.orig_img = self.image
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

    def update(self):
        self.rotate()
        self.pos += self.vel
        self.hitbox.centerx = self.pos.x
        self.collide_with_tiles(self.walls, "x")
        self.hitbox.centery = self.pos.y
        self.collide_with_tiles(self.walls, "y")
        self.rect.center = self.pos

    def rotate(self):
        rel_x, rel_y = pygame.mouse.get_pos() - self.pos
        angle = -math.degrees(math.atan2(rel_y, rel_x))
        self.image = pygame.transform.rotate(self.orig_img, int(angle))
        self.rect = self.image.get_rect(center=self.pos)

    def collide_with_tiles(self, group, dir):
        if dir == "x":
             for wall in self.walls:
                 if self.hitbox.colliderect(wall.rect):
                     if self.vel.x > 0:
                         self.hitbox.right = wall.rect.left
                     if self.vel.x < 0:
                         self.hitbox.left = wall.rect.right
                     self.vel.x = 0
                     self.pos.x = self.hitbox.centerx

        if dir == "y":
            for wall in self.walls:
                if self.hitbox.colliderect(wall.rect):
                    if self.vel.y > 0:
                        self.hitbox.bottom = wall.rect.top
                    if self.vel.y < 0:
                        self.hitbox.top = wall.rect.bottom
                    self.vel.y = 0
                    self.pos.y = self.hitbox.centery


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color('sienna1'))
        self.rect = self.image.get_rect(topleft=(x, y))


def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    sprite_group = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    wall = Wall(100, 200, 300, 30)
    walls.add(wall)
    sprite_group.add(wall)

    player = Player(300, 400, walls)
    sprite_group.add(player)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.vel.y = -3
                elif event.key == pygame.K_s:
                    player.vel.y = 3
                elif event.key == pygame.K_a:
                    player.vel.x = -3
                elif event.key == pygame.K_d:
                    player.vel.x = 3
            elif event.type == pygame.KEYUP:
                player.vel = vec(0, 0)

        sprite_group.update()
        screen.fill((30, 30, 30))
        sprite_group.draw(screen)
        pygame.draw.rect(screen, (200, 30, 30), player.rect, 2)
        pygame.draw.rect(screen, (0, 200, 30), player.hitbox, 2)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
rel_x, rel_y = pg.mouse.get_pos() - vec(self.camera.apply(self).center)