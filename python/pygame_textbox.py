import pygame

pygame.init()


class textecreate:
    def __init__(self, text, font, coords: tuple, color, text_align='center'):
        self.font = font
        self.x, self.y = coords[0], coords[1]
        self.color = color

        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect()
        self.text_align = text_align

        self.align()

    def align(self):
        if self.text_align == 'center':
            self.rect.centerx = self.x
        elif self.text_align == 'left':
            self.rect.x = self.x
        self.rect.y = self.y


class textealign:
    def __init__(self, text, font: tuple, coords: tuple, color, text_align='center', space_size=1, separator='\n'):
        self.text = text
        self.separator = separator
        self.x, self.y = coords[0], coords[1]
        self.text_align = text_align
        try:
            self.font = pygame.font.Font(font[0], font[1])
        except FileNotFoundError:
            self.font = pygame.font.SysFont(font[0], font[1])

        self.color = color
        self.space_size = space_size
        self.liste = self.text.split(self.separator)
        print(self.liste)
        self.nbligne = len(self.liste)
        self.create(self.x, self.y)

    def create(self, x1, y1):
        self.d = {}
        x = x1
        y = y1
        for element in range(len(self.liste)):
            self.d[str(element)] = textecreate(self.liste[element], self.font, (x, y), self.color, self.text_align)
            y += self.font.size(self.liste[element])[1] * self.space_size

    def update(self, coords):
        x, y = coords[0], coords[1]
        self.create(x, y)

    def get_size(self):
        calc = self.nbligne * self.font.size(self.liste[0])[1] * self.space_size
        return calc

    def iblit(self, screen):
        for i in self.d.keys():
            screen.blit(self.d[i].text, self.d[i].rect)
