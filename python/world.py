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

		self.dirtlayerheight = 5
		self.surfaceValue = -0.225

		self.generateCave = True
		self.seed = random.randint(-10000, 10000)
		self.worldsize = 150
		self.CaveFreq = 0.08
		self.TerrainFreq = 0.02
		self.heightmultiplier = 25
		self.heightaddtion = 25

		self.treechance = 10

		self.width = 1200
		self.height = 800
		self.map = []


	def generate(self):
		pass

	def GenerateNoiseTexture(self):
		pic = []
		for i in range(self.worldsize):
			row = []
			for j in range(self.worldsize):
				noise_val = noise.pnoise2((i + self.seed) * self.CaveFreq, (j + self.seed) * self.CaveFreq, 2, 0.5, 2,
										  1024, 1024)
				print(noise_val)
				row.append(noise_val)
			pic.append(row)
		print('Gen noise finished')
		return pic

	def GenerateTerrain(self):
		x = 0
		noiseeffet = self.GenerateNoiseTexture()
		while x < self.worldsize:
			y = 0
			height = noise.pnoise2((x + self.seed) * self.TerrainFreq, self.seed * self.TerrainFreq, 2, 0.5, 2, 1024,
								   1024) * self.heightmultiplier + self.heightaddtion
			while y < height:
				if (y < height - self.dirtlayerheight + random.randint(-1, 1)):
					element = 'stone'
				elif y < height - 1:
					element = 'dirt'
				else:
					# Generation herbe
					element = 'grass'
				if self.generateCave:
					if noiseeffet[x][y] > self.surfaceValue:
						self.PlaceTile(x, y, element)
				else:
					self.PlaceTile(x, y, element)
				y += 1
			x += 1

		while x < self.worldsize:
			y = 0
			height = noise.pnoise2((x + self.seed) * self.TerrainFreq, self.seed * self.TerrainFreq, 2, 0.5, 2, 1024,
								   1024) * self.heightmultiplier + self.heightaddtion
			while y < height:
				if (y < height - self.dirtlayerheight + random.randint(-1, 1)):
					print('couche herbe')
				elif y < height - 1:
					print('couche terre')
				else:
					# Generation herbe
					self.tree = random.randint(0, self.treechance)

					if self.tree == 1:
						# Generation d'un arbre
						self.GenerateTree(x, y + 1)
				y += 1
			x += 1

		print('Gen map Finished')

		return self.map

	def PlaceTile(self, x, y, element):
		self.map += [[[x, -y], element]]

	def GenerateTree(self, x, y):
		return self.PlaceTile(x, y, 'trunk_bottom')