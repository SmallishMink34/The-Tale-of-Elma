import pygame, sys, os, random, noise
from pygame.locals import *
from perlin_noise import PerlinNoise


class tiles(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		super().__init__()
		self.image = pygame.image.load(image).convert_alpha()
		self.size = 8
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y

	def iblit(self, screen):
		screen.blit(self.image, self.rect)

	'''def __repr__(self):
		return str([self.rect.x, self.rect.y])'''


class Terrain:
	def __init__(self):
		self.seed = 2004
		self.worldsize = 100
		self.noiseFreq = 0.05
		self.width = 1200
		self.height = 800
		self.heightmultiplier = 80

	def generate(self):
		pass

	def GenerateNoiseTexture(self):
		noise1 = PerlinNoise(octaves=3, seed=self.seed)
		noise2 = PerlinNoise(octaves=6, seed=self.seed)
		noise3 = PerlinNoise(octaves=12, seed=self.seed)
		noise4 = PerlinNoise(octaves=24, seed=self.seed)
		pic = []
		for i in range(self.worldsize):
			row = []
			for j in range(self.worldsize):
				noise_val = noise1([i / self.worldsize, j / self.worldsize])
				noise_val += 0.5 * noise2([i / self.worldsize, j / self.worldsize])
				noise_val += 0.25 * noise3([i / self.worldsize, j / self.worldsize])
				noise_val += 0.125 * noise4([i / self.worldsize, j / self.worldsize])

				row.append(noise_val)
			pic.append(row)
		print('Gen noise finished')
		return pic

	def GenerateTerrain(self):
		x = 0
		noiseeffet = self.GenerateNoiseTexture()
		map = []
		while x < self.worldsize:
			y = 0
			height = PerlinNoise(octaves=4.8, seed=self.seed)
			height_val = abs(height([(x + self.seed) * self.noiseFreq, self.seed * self.noiseFreq]) * self.heightmultiplier)
			print(height_val)
			while y < height_val:
				map += [[[x, y], 1]]
				'''if noiseeffet[x][y] < 0.05:
					pass
				else:
					pass
					map += [[[x, y], 0]]'''
				y += 1
			x += 1
		print('Gen map Finished')

		return map
