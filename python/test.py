import pygame
import random

pygame.init()

screen = pygame.display.set_mode((500, 500))

# these are the images that get shown as items, different color circle for each item
items = [pygame.Surface((50, 50), pygame.SRCALPHA) for x in range(4)]
pygame.draw.circle(items[0], (255, 0, 0), (25, 25), 25)
pygame.draw.circle(items[1], (0, 255, 0), (25, 25), 25)
pygame.draw.circle(items[2], (255, 255, 0), (25, 25), 25)
pygame.draw.circle(items[3], (0, 0, 255), (25, 25), 25)

font = pygame.font.Font(pygame.font.match_font("calibri"), 26)


# class for a item, just holds the surface and can resize it
class Item:
    def __init__(self, id):
        self.id = id
        self.surface = items[id]

    def resize(self, size):
        return pygame.transform.scale(self.surface, (size, size))


# the inventory system
class Inventory:
    def __init__(self):
        self.rows = 3
        self.col = 9
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 40
        self.x = 50
        self.y = 50
        self.border = 3

    # draw everything
    def draw(self):
        # draw background
        pygame.draw.rect(screen, (100, 100, 100),
                         (self.x, self.y, (self.box_size + self.border) * self.col + self.border,
                          (self.box_size + self.border) * self.rows + self.border))
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border) * x + self.border,
                        self.x + (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                pygame.draw.rect(screen, (180, 180, 180), rect)
                if self.items[x][y]:
                    screen.blit(self.items[x][y][0].resize(self.box_size), rect)
                    obj = font.render(str(self.items[x][y][1]), True, (0, 0, 0))
                    screen.blit(obj, (rect[0] + self.box_size // 2, rect[1] + self.box_size // 2))

    # get the square that the mouse is over
    def Get_pos(self):
        mouse = pygame.mouse.get_pos()

        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x // (self.box_size + self.border)
        y = y // (self.box_size + self.border)
        return (x, y)

    # add an item/s
    def Add(self, Item, xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].id == Item[0].id:
                self.items[x][y][1] += Item[1]
            else:
                temp = self.items[x][y]
                self.items[x][y] = Item
                return temp
        else:
            self.items[x][y] = Item

    # check whether the mouse in in the grid
    def In_grid(self, x, y):
        if 0 > x > self.col - 1:
            return False
        if 0 > y > self.rows - 1:
            return False
        return True


player_inventory = Inventory()

# what the player is holding
selected = None

running = True
while running:
    # draw the screen
    screen.fill((255, 255, 255))
    player_inventory.draw()

    mousex, mousey = pygame.mouse.get_pos()

    # if holding something, draw it next to mouse
    if selected:
        screen.blit(selected[0].resize(30), (mousex, mousey))
        obj = font.render(str(selected[1]), True, (0, 0, 0))
        screen.blit(obj, (mousex + 15, mousey + 15))

    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            # if right clicked, get a random item
            if e.button == 3:
                selected = [Item(random.randint(0, 3)), 1]
            elif e.button == 1:
                pos = player_inventory.Get_pos()
                if player_inventory.In_grid(pos[0], pos[1]):
                    if selected:
                        selected = player_inventory.Add(selected, pos)
                    elif player_inventory.items[pos[0]][pos[1]]:
                        selected = player_inventory.items[pos[0]][pos[1]]
                        player_inventory.items[pos[0]][pos[1]] = None