import pygame, sys, os, random, noise


class tiles(pygame.sprite.Sprite):
	def __init__(self, name, image, x, y, posinworld =[0, 0],size=16):
		super().__init__()
		self.name = name
		self.posinworld = posinworld
		self.image = pygame.image.load(image).convert_alpha()
		self.size = size
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y

	def getcoords(self):
		return (round(self.rect.x / self.size), round(self.rect.y / self.size))

	def die(self):
		self.kill()

	def __repr__(self):
		return self.name


class Terrain:
	def __init__(self):

		self.dirtlayerheight = 5
		self.surfaceValue = -0.225
		self.basevalue = 0

		self.generateCave = True
		self.seed = 5 #random.randint(-10000, 10000)
		self.worldsize = 150
		self.CaveFreq = 0.08
		self.TerrainFreq = 0.02
		self.heightmultiplier = 25
		self.heightaddtion = 40

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
						if self.map[x][y][1] == 'grass':
							self.GenerateTree(x, y + 1)
				y += 1

			x += 1

		print('Gen map Finished')
		return self.map

	def newmap(self, mape):
		self.map = mape
		return self.map

	def PlaceTile(self, x, y, element):
		self.ligne += [[[x, -y], element]]

	def ReplaceTile(self, x, y, element, playermode=False):
		if playermode and element != 'air':
			for i in range(len(self.map)):
				if i == x:
					for i2 in range(len(self.map[x])):
						if i2 == y:
							if self.map[x][y][1] == 'air':
								self.map[x][y] = [[x, -y], element]

		else:
			for i in range(len(self.map)):
				if i == x:
					for i2 in range(len(self.map[x])):
						if i2 == y:
							self.map[x][y] = [[x, -y], element]

	def GenerateTree(self, x, y):
		tree_file = open('../structure/arbre_1.txt', 'r')
		tree_list = tree_file.readlines()
		tree_file.close()

		for element in range(len(tree_list)):
			tree_list[element] = tree_list[element].strip().split(',')


		x2 = -round(len(tree_list[0]) / 2)
		i = 0
		y2 = -len(tree_list)+1
		for row in tree_list:
			for column in row:
				print(x2, y2)
				self.ReplaceTile(x-x2, y-y2, column)
				x2+=1
				i+= 1
			y-=1
			x2= -round(len(tree_list[x2]) / 2)
			i = 0
