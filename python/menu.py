import game
import ClassPG as PG
import pygame
import ast
import pygame_widgets as pw
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.toggle import Toggle
from valeurs import *


class menu():
    def __init__(self, val) -> None:
        self.start()
        self.display_w, self.display_h = self.w, self.h
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60, self.fullscreen)
        self.display = pygame.Surface((self.display_w, self.display_h))

        self.val = val
        self.d = {}
        self.load()
        self.paraa = para(self, self.val)

    def gameloop(self, event, screen):
        self.eventpy(event)
        self.iblit(screen)

    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['text_Play'].click((x, y), event, color=(128, 255, 0)):
                self.continuer = False
                gamee = game.Game((self.val.screensize[0], self.val.screensize[1], self.val.toggle))
                self.val.musique.stop()
                gamee.run()
            if self.d['text_Quit'].click((x, y), event, color=(128, 255, 0)):
                pygame.quit()
            if self.d['text_Para'].click((x, y), event, color=(128, 255, 0)):
                self.continuer = False
                self.paraa.load()
                self.paraa.run()

    def start(self):
        set = open("../python/save/settings.txt", "r")
        L = set.readlines()
        self.w, self.h = int(L[1].split(" ")[1].split(",")[0]), int(L[1].split(" ")[1].split(",")[1])
        self.fullscreen = False if L[2].split(" ")[1] == "False" else True
        set.close()

    def load(self):
        set = open("../python/save/settings.txt", "r")
        L = set.readlines()
        self.val.musique.volume(round(float(L[0].split(" ")[1]), 2))
        self.val.screensize2((int(L[1].split(" ")[1].split(",")[0]), int(L[1].split(" ")[1].split(",")[1])),
                             self.game.screen, self.val.toggle)
        self.d['text_Play'] = PG.Texte("Jouer", self.val.screensize[0] // 2 - 100, self.val.screensize[1] // 2 - 10,
                                       True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['text_Para'] = PG.Texte("Parametres", self.val.screensize[0] // 2 - 100,
                                       self.val.screensize[1] // 2 + 100, True, color=(255, 255, 255), size=50,
                                       font='../font/Like Snow.otf')
        self.d['text_Quit'] = PG.Texte("Quitter", self.val.screensize[0] // 2 - 100, self.val.screensize[1] // 2 + 210,
                                       True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['Titre'] = PG.Texte("Titre", self.val.screensize[0] // 2 - 175, self.val.screensize[1] // 2 - 275, True,
                                   color=(255, 255, 255), size=125, font='../font/Like Snow.otf')
        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)
        self.display = pygame.Surface(self.val.screensize)
        set.close()

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)

    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.display, (0, 0))
            self.gameloop(pygame.event.get(), self.display)
            pygame.display.update()
        pygame.quit()


class para():
    def __init__(self, menu, val) -> None:
        self.display_w, self.display_h = menu.w, menu.h

        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60, menu.fullscreen)
        self.val = val
        self.d = {}
        self.load()
        self.musi = song(menu, self.val)
        self.menuu = menu
        self.touche = Touches(menu, self.val)

    def gameloop(self, event, screen):
        self.eventpy(event)
        self.iblit(screen)

    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x, y), event):
                self.continuer = False
                self.menuu.run()
            if self.d['Musique'].click((x, y), event):
                self.musi.load()
                self.musi.run()
            if self.d['Touche'].click((x, y), event):
                self.touche.load()
                self.touche.run()

    def load(self):
        set = open("../python/save/settings.txt", "r")
        L = set.readlines()
        self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)

        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 40, 50, 50)
        self.d['Musique'] = PG.Texte("General", self.val.screensize[0] // 2 - 100, self.val.screensize[1] // 2 - 10,
                                     True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['Touche'] = PG.Texte("Touches", self.val.screensize[0] // 2 - 100, self.val.screensize[1] // 2 + 100,
                                    True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['Skin'] = PG.Texte("Cosmetiques", self.val.screensize[0] // 2 - 100, self.val.screensize[1] // 2 + 210,
                                  True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)

    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.game.screen, (0, 0))
            self.gameloop(pygame.event.get(), self.game.screen)
            pygame.display.update()
        pygame.quit()


class song():
    def __init__(self, menu, val) -> None:
        self.display_w, self.display_h = menu.w, menu.h
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60, menu.fullscreen)
        self.val = val

        self.slider = Slider(self.game.screen, self.val.screensize[0] // 2 - 400, self.val.screensize[1] // 2 + 30, 800,
                             40, min=0, max=99, step=1, initial=0, curved=True, handleRadius=30)
        self.dropdown = Dropdown(self.game.screen, self.val.screensize[0] // 2 - 100, self.val.screensize[1] // 2 - 300,
                                 200, 100, name='Resolution',
                                 choices=[
                                     '1920x1080',
                                     '1366x768',
                                     '1280x720', ], borderRadius=3, colour=pygame.Color('white'),
                                 values=[(1920, 1080), (1366, 768), (1280, 720)], direction='down', textHAlign='centre')
        self.toggle = Toggle(self.game.screen, self.val.screensize[0] // 2 - 25, self.val.screensize[1] // 2 - 55, 60,
                             20, onColour=(255, 255, 255), offColour=(0, 0, 0), handleOnColour=(200, 200, 200))
        self.load()
        self.menu = menu

    def gameloop(self, event, screen):
        self.iblit(screen)
        self.eventpy(event)

    def eventpy(self, events):
        for event in events:
            self.d['Volume'].iupdate("Volume : " + str(self.slider.getValue()) + "%", (255, 255, 255),
                                     (self.val.screensize[0] // 2 - 85, self.val.screensize[1] // 2 + 130))
            self.val.volume = self.slider.getValue() / 100
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x, y), event):
                self.continuer = False
                self.menu.load()
                self.val.save()
                self.menu.run()
            if self.d['Valider'].click((x, y), event):
                self.changescreensize()
                self.val.save()
                self.menu.load()
        pw.update(events)

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)

    def load(self):
        # slider 
        set = open("../python/save/settings.txt", "r")
        L = set.readlines()
        self.val.toggle = ast.literal_eval(L[2].split(" ")[1])
        self.game.screen = self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)
        self.volume = self.val.volume
        self.slider.setValue(float(L[0].split(" ")[1]) * 100)
        self.slider._x = self.val.screensize[0] // 2 - 400
        self.slider._y = self.val.screensize[1] // 2 + 40
        self.dropdown._x = self.val.screensize[0] // 2 - 100
        self.dropdown._y = self.val.screensize[1] // 2 - 300
        self.toggle._x = self.val.screensize[0] // 2 - 25
        self.toggle._y = self.val.screensize[1] // 2 - 55
        self.d = {}
        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 40, 50, 50)
        self.d['Volume'] = PG.Texte('Volume : 0', self.val.screensize[0] // 2 - 85, self.val.screensize[1] // 2 + 130,
                                    False)
        self.d['Valider'] = PG.Texte("Valider", self.val.screensize[0] / 2 - 40, self.val.screensize[1] - 100, True,
                                     color=(0, 0, 0), size=32)
        self.d['Toggle'] = PG.Texte("Fullscreen : ", self.val.screensize[0] // 2 - 85,
                                    self.val.screensize[1] // 2 - 135, True, color=(255, 255, 255), size=32)
        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)

    def changescreensize(self):
        if self.dropdown.getSelected() != None:
            self.val.screensize2(self.dropdown.getSelected(), self.game.screen, self.toggle.getValue())
            self.val.save()
            self.load()

    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.game.screen, (0, 0))
            self.gameloop(pygame.event.get(), self.game.screen)
            pygame.display.update()
        pygame.quit()


class Touches():
    def __init__(self, menu, val) -> None:
        self.display_w, self.display_h = menu.w, menu.h
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60, menu.fullscreen)
        self.val = val

        self.load()
        self.menu = menu
        self.stat = False

    def gameloop(self, event, screen):
        self.iblit(screen)
        self.eventpy(event)

    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x, y), event):
                self.continuer = False
                self.menu.load()
                self.val.save()
                self.menu.run()
            for i in self.touchec:
                if i.click((x, y), event) and self.stat == False:
                    self.stat = True
                    i.stats = True

            if self.stat == True:
                for i in self.touchec:
                    if i.stats == True:
                        if event.type == pygame.KEYDOWN:
                            i.change(str(pygame.key.name(event.key)))
                            i.stats = False
                            self.val.l[i.name] = pygame.key.key_code(pygame.key.name(event.key))
                            self.stat = False
                            print(self.val.l)

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)
        for i in self.touchec:
            i.iblit(screen)

    def load(self):
        # slider
        set = open("../python/save/keybinding.txt", "r")
        L = set.readlines()
        self.game.screen = self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)

        self.d = {}
        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 40, 50, 50)

        for i in self.val.l.keys():
            for i2 in L:
                if i in i2.strip().split(":")[0]:
                    print(pygame.key.name(int(i2.strip().split(":")[1].strip())))
                    self.val.l[i] = pygame.key.key_code(pygame.key.name(int(i2.strip().split(":")[1].strip())))

        print(self.val.l)
        x = 500
        y = 120
        self.touchec = []
        for i in self.val.l.keys():
            self.touchec.append(keys(i, x, y, pygame.key.name(self.val.l[i])))
            y += 70

        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)

    def changescreensize(self):
        if self.dropdown.getSelected() != None:
            self.val.screensize2(self.dropdown.getSelected(), self.game.screen, self.toggle.getValue())
            self.val.save()
            self.load()

    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.game.screen, (0, 0))
            self.gameloop(pygame.event.get(), self.game.screen)
            pygame.display.update()
        pygame.quit()


class keys():
    def __init__(self, name, x, y, keys: str):
        self.x, self.y = x, y
        self.name = name
        self.txt = PG.Texte(name + ' : ' + str(keys), x, y, False)
        self.stats = False

    def click(self, mousepos, event):
        return self.txt.click(mousepos, event)

    def change(self, keys):
        self.txt = PG.Texte(self.name + ' : ' + str(keys), self.x, self.y, False)

    def iblit(self, screen):
        self.txt.iblit(screen)


menue = menu(valeur)
menue.run()
