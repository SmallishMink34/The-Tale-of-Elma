import pygame, sys, os, random, noise
from pygame.locals import *

class tiles(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (48,48))
        
    
    def setcoord(self, x,y):
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y 
    
    def iblit(self, screen):
        screen.blit(self.image, self.rect)



def generate_chunk(x, y):
    Chunk_size = 8
    chunk = []
    for y_pos in range(Chunk_size):
        for x_pos in range(Chunk_size):
            target_x = x*Chunk_size+x_pos
            target_y = y*Chunk_size+y_pos
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)
            tile_type = 0
            if target_y > 8 - height:
                tile_type = 1
            elif target_y == 8 - height:
                tile_type = 2
            elif target_y == 8 - height - 1:
                if random.randint(1,5) == 1:
                    tile_type = 3
            if tile_type != 0:
                chunk.append([[target_x, target_y], tile_type])
                
    return chunk