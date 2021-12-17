import pygame, sys, os, random, noise
import ClassPlayer

cp = ClassPlayer.Player()
class tiles(pygame.sprite.Sprite):
	def __init__(self, name, image, x, y, size=16):
		super().__init__()
		self.name = name
		self.image = pygame.image.load(image).convert_alpha()
		self.size = size
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
	def set_coord(self,x,y):
		self.rect.x, self.rect.y = x, y
		
	def getcoords(self):
		return (round(self.rect.x / self.size), round(self.rect.y / self.size))

	def __repr__(self):
		return self.name


class Terrain:
	def __init__(self):

		self.dirtlayerheight = 5
		self.surfaceValue = -0.225
		self.basevalue = 0

		self.generateCave = True
		self.seed = random.randint(-10000, 10000)
		self.worldsize = 30
		self.CaveFreq = 0.08
		self.TerrainFreq = 0.02
		self.heightmultiplier = 25
		self.heightaddtion = 25

		self.treechance = 10

		self.width = 1200
		self.height = 800
		self.ligne = []
		self.map = [self.ligne]*self.worldsize


	def generate(self):
		pass

	def GenerateNoiseTexture(self):
		pic = []
		for i in range(self.worldsize):
			row = []
			for j in range(self.worldsize):
				noise_val = noise.pnoise2((i + self.seed) * self.CaveFreq, (j + self.seed) * self.CaveFreq, 2, 0.5, 2,
										  1024, 1024)
				row.append(noise_val)
			pic.append(row)
		print('Gen noise finished')
		return pic

	def GenerateTerrain(self):
		x = 0
		noiseeffet = self.GenerateNoiseTexture()
		while x < self.worldsize :
			y = 0
			height = noise.pnoise2((x + self.seed) * self.TerrainFreq, self.seed * self.TerrainFreq, 2, 0.5, 2, 1024,
								   1024) * self.heightmultiplier + self.heightaddtion
			while y < self.worldsize:
				if (y < height - self.dirtlayerheight + random.randint(-1, 1)):
					element = 'stone'
				elif y < height - 1:
					element = 'dirt'
				elif y < height:
					element = 'grass'
				else:
					element = 'air'

				if self.generateCave:
					if noiseeffet[x][y] > self.surfaceValue:
						self.PlaceTile(x, y, element)
					else:
						self.PlaceTile(x, y, 'air')
				else:
					self.PlaceTile(x, y, element)
				y += 1

			self.map[x] = self.ligne
			self.ligne = []
			x += 1

		x = 0
		while x < self.worldsize:
			y = 0
			height = noise.pnoise2((x + self.seed) * self.TerrainFreq, self.seed * self.TerrainFreq, 2, 0.5, 2, 1024,
								   1024) * self.heightmultiplier + self.heightaddtion
			self.ligne = self.map[x]
			while y < height:
				if (y < height - self.dirtlayerheight + random.randint(-1, 1)):
					pass
				elif y < height - 1:
					pass
				else:
					# Generation herbe
					self.tree = random.randint(0, self.treechance)

					if self.tree == 1 :
						# Generation d'un arbre
						print(self.map[0][0][1])
						if self.map[x][y][1] == 'grass':
							self.GenerateTree(x, y + 1)

				y += 1
			self.map[x] = self.ligne
			x += 1

		print('Gen map Finished')
		return self.map

	def PlaceTile(self, x, y, element):
		self.ligne += [[[x, -y], element]]

	def GenerateTree(self, x, y):
		self.PlaceTile(x, y, 'trunk_bottom')
		self.PlaceTile(x, y+1, 'trunk_mid')
		self.PlaceTile(x, y+2, 'trunk_mid')
		self.PlaceTile(x, y+3, 'trunk_side')
		self.PlaceTile(x-1, y + 3, 'leaves')
		self.PlaceTile(x , y + 4, 'leaves')
		self.PlaceTile(x + 1, y + 3, 'leaves')