import pygame, sys, os, random, noise
from pygame.locals import *


class tiles(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		super().__init__()
		self.image = pygame.image.load(image).convert_alpha()
		self.size = 16
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y

	def iblit(self, screen):
		screen.blit(self.image, self.rect)

	'''def __repr__(self):
		return str([self.rect.x, self.rect.y])'''


def generate_chunk(x, y):
	Chunk_size = 16
	chunk = []
	for y_pos in range(Chunk_size):
		for x_pos in range(Chunk_size):
			target_x = x * Chunk_size + x_pos
			target_y = y * Chunk_size + y_pos
			height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)
			tile_type = 0
			if target_y > 8 - height:
				tile_type = 1
			elif target_y == 8 - height:
				tile_type = 2
			elif target_y == 8 - height - 1:
				if random.randint(1, 5) == 1:
					tile_type = 3
			if tile_type != 0:
				chunk.append([[target_x, target_y], tile_type])

	return chunk


def Genlist(width, height, empty):
	x = 0
	map = [[[0, 0], 1]]
	while x <= width:
		y = 0
		while y <= height:

			map += [[[x, y], 1]]
			if empty:
				map[x][1] = 0
			else:
				map[x][1] = 1
			y += 1
		x += 1
	return map
