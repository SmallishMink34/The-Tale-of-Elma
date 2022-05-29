# Importation des modules nécessaires à l'exécution du programme.
import game
import ClassPG as PG
import pygame
import moviepy.editor
import ast
import pygame_widgets as pw
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.toggle import Toggle
import valeurs
import math
import os
import threading


class menu():
    def __init__(self, val) -> None:
        self.val = val

        self.w, self.h = self.val.screensize[0], self.val.screensize[1]
        self.fullscreen = self.val.toggle
        self.display_w, self.display_h = self.val.screensize[0], self.val.screensize[1]
        self.game = PG.game("Ingame", self.val.screensize, 60, self.val.toggle)
        self.display = pygame.Surface((self.display_w, self.display_h))

        self.d = {}
        self.load()
        self.val.musique.play()

        self.paraa = para(self, self.val)
        self.choosemenu = Choose_save(self, self.val)

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
                self.val.musique.stop()
                self.choosemenu.load()
                self.choosemenu.run()
                """gamee = game.Game((self.val.screensize[0], self.val.screensize[1], self.val.toggle))
                gamee.run()"""
            if self.d['text_Quit'].click((x, y), event, color=(128, 255, 0)):
                pygame.quit()
            if self.d['text_Para'].click((x, y), event, color=(128, 255, 0)):
                self.continuer = False
                self.paraa.load()
                self.paraa.run()

    def load(self):
        set = open("Basesave/settings.txt", "r")
        L = set.readlines()
        self.val.musique.volume(round(float(L[0].split(" ")[1]), 2))
        self.val.screensize2((int(L[1].split(" ")[1].split(",")[0]), int(L[1].split(" ")[1].split(",")[1])),
                             self.game.screen, self.val.toggle)
        self.d['text_Play'] = PG.Texte("Jouer", self.val.screensize[0] // 2, self.val.screensize[1] // 2 - 10,
                                       True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['text_Para'] = PG.Texte("Parametres", self.val.screensize[0] // 2,
                                       self.val.screensize[1] // 2 + 100, True, color=(255, 255, 255), size=50,
                                       font='../font/Like Snow.otf')
        self.d['text_Quit'] = PG.Texte("Quitter", self.val.screensize[0] // 2, self.val.screensize[1] // 2 + 210,
                                       True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        """self.d['Titre'] = PG.Texte("Titre", self.val.screensize[0] // 2, self.val.screensize[1] // 2 - 275, True,
                                   color=(255, 255, 255), size=125, font='../font/Like Snow.otf')"""

        self.d['Titre'] = PG.img("../img/Titre.png", 0, -120 * self.val.facteur, self.val.screensize[0],
                                 self.val.screensize[1], False)

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
        print(self.val.screensize)
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
        set = open("Basesave/settings.txt", "r")
        L = set.readlines()
        self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)

        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 60, 50, 50)
        self.d['Musique'] = PG.Texte("General", self.val.screensize[0] // 2, self.val.screensize[1] // 2 - 10,
                                     True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['Touche'] = PG.Texte("Touches", self.val.screensize[0] // 2, self.val.screensize[1] // 2 + 100,
                                    True, color=(255, 255, 255), size=50, font='../font/Like Snow.otf')
        self.d['Skin'] = PG.Texte("Cosmetiques", self.val.screensize[0] // 2, self.val.screensize[1] // 2 + 210,
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
                                     (self.val.screensize[0] // 2, self.val.screensize[1] // 2 + 130))
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
        set = open("Basesave/settings.txt", "r")
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
        self.toggle.value = self.val.toggle
        self.d = {}
        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 60, 50, 50)
        self.d['Volume'] = PG.Texte('Volume : 0', self.val.screensize[0] // 2, self.val.screensize[1] // 2 + 130,
                                    True)
        self.d['Valider'] = PG.Texte("Valider", self.val.screensize[0] / 2, self.val.screensize[1] - 100, True,
                                     color=(0, 0, 0), size=32)
        self.d['Toggle'] = PG.Texte("Fullscreen : ", self.val.screensize[0] // 2,
                                    self.val.screensize[1] // 2 - 135, True, color=(255, 255, 255), size=32)
        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)

    def changescreensize(self):
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

        self.last_key = None

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
                    i.change_stats(True)
                    self.last_key = i
                if i.click((x, y), event) and self.stat:
                    self.last_key.change_stats(False)
                    i.change_stats(True)
                    self.last_key = i

            if self.stat == True:
                for i in self.touchec:
                    if i.stats == True:
                        if event.type == pygame.KEYDOWN:
                            i.change(str(pygame.key.name(event.key)))
                            i.change_stats(False)
                            self.val.l[i.name] = pygame.key.key_code(pygame.key.name(event.key))
                            self.stat = False

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)
        for i in self.touchec:
            i.iblit(screen)

    def load(self):
        # slider
        set = open("Basesave/keybinding.txt", "r")
        L = set.readlines()
        self.game.screen = self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)

        self.d = {}
        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 40, 50, 50)

        for i in self.val.l.keys():
            for i2 in L:
                if i in i2.strip().split(":")[0]:
                    self.val.l[i] = pygame.key.key_code(pygame.key.name(int(i2.strip().split(":")[1].strip())))

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


class ChoosePlayer():
    def __init__(self, menu, val, save: str) -> None:
        self.val = val
        self.display_w, self.display_h = self.val.screensize[0], self.val.screensize[1]
        print(self.display_w, self.display_h)

        self.game = PG.game("ChoosePlayer", (self.display_w, self.display_h), 60, self.val.toggle)

        self.d = {}

        self.menuu = menu

        self.savee = save
        self.movie()
        self.load()

    def movie(self):
        self.Film = moviepy.editor.VideoFileClip("../img/Intro.mp4")
        self.Film_resized = self.Film.resize(self.val.screensize)
        self.Film = self.Film_resized
        self.Film.set_fps(60)

    def gameloop(self, event, screen):
        self.iblit(screen)
        self.eventpy(event, screen)

    def change_save_stat(self):
        w = open("Basesave/save.txt", "r")
        l = w.readlines()
        w.close()

        w = open("Basesave/save.txt", "w")
        for i in l:
            if self.savee in i:
                w.write(self.savee + ": True\n")

            else:
                w.write(i)
        w.close()

    def eventpy(self, events, screen):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x, y), event):
                self.continuer = False
                self.menuu.run()
            if self.d["TextName"].select:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.Film.preview(fullscreen=self.val.toggle)
                        self.val.name = self.d['TextName'].get_text()
                        self.change_save_stat()
                        gamee = game.Game((self.val.screensize[0], self.val.screensize[1], self.val.toggle))
                        gamee.map_manag.save("Lobby")
                        gamee.map_manag.maps["Lobby"].mapobject.allmap.save_player_info()
                        gamee.run()

        self.d['TextName'].iblit(events, screen)

    def load(self):
        set = open("Basesave/settings.txt", "r")
        L = set.readlines()
        self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)

        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 60, 50, 50)
        self.d['Name'] = PG.Texte('Pseudo : ', self.val.screensize[0] / 2, 320 * self.val.facteur, True,
                                  (255, 255, 255), 32, "../font/Like Snow.otf")
        self.d['TextName'] = PG.TextEntry(self.menuu.display, (255, 255, 255),
                                          (self.val.screensize[0] / 2, 360 * self.val.facteur, 320, 40), 'text', True)

        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            if i != "TextName":
                self.d[i].iblit(screen)

    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.game.screen, (0, 0))
            self.gameloop(pygame.event.get(), self.game.screen)
            pygame.display.update()
        pygame.quit()


class Choose_save():
    def __init__(self, menu, val) -> None:
        self.val = val
        self.display_w, self.display_h = self.val.screensize[0], self.val.screensize[1]

        self.game = PG.game("ChooseSave", (self.display_w, self.display_h), 60, self.val.toggle)

        self.d = {}

        self.menuu = menu
        self.touche = Touches(menu, self.val)
        self.load()
        self.d['delete'] = PG.bouton("../img/menu/trash.png", 1210, 660, 60, 60, True, True, True)
        self.delete = False

    def gameloop(self, event, screen):
        self.iblit(screen)
        self.eventpy(event, screen)

    def delete_save(self, savename):
        dir1 = savename + "/save/"
        dir2 = savename + "/save.inv/"

        for i in os.listdir(dir1):
            os.remove(os.path.join(dir1, i))
        for i in os.listdir(dir2):
            os.remove(os.path.join(dir2, i))

    def eventpy(self, events, screen):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x, y), event):
                self.continuer = False
                self.menuu.run()
            if self.d['delete'].click((x, y), event):
                self.delete = not self.d['delete'].toggle_verif
                for i in self.d.keys():
                    if 'save' in i:
                        self.d[i].shaking = self.delete

            if self.d['save1'].click((x, y), event):
                if not self.delete:
                    if not self.d['save1'].save:
                        self.val.save_l = self.d['save1'].savename
                        a = ChoosePlayer(self.menuu, self.val, 'save1')
                        a.run()
                    else:
                        self.val.save_l = self.d['save1'].savename
                        self.val.name = self.d['save1'].pseudo
                        gamee = game.Game((self.val.screensize[0], self.val.screensize[1], self.val.toggle))
                        gamee.run()
                else:
                    try:
                        self.delete_save("first")
                        self.dico['save1'] = str(False)
                        self.save()
                        self.load()
                        for i in self.d.keys():
                            if 'save' in i:
                                self.d[i].shaking = self.delete
                    except FileNotFoundError:
                        pass
            if self.d['save2'].click((x, y), event):
                if not self.delete:
                    if not self.d['save2'].save:
                        self.val.save_l = self.d['save2'].savename
                        a = ChoosePlayer(self.menuu, self.val, 'save2')
                        a.run()
                    else:
                        self.val.save_l = self.d['save2'].savename
                        self.val.name = self.d['save2'].pseudo
                        gamee = game.Game((self.val.screensize[0], self.val.screensize[1], self.val.toggle))
                        gamee.run()
                else:
                    try:
                        self.delete_save("second")
                        # Créer un dictionnaire avec les clés 'save1' et 'save2' et leur attribuer les valeurs 'True' et
                        # 'False'.
                        self.dico['save2'] = str(False)
                        self.save()
                        self.load()
                        for i in self.d.keys():
                            if 'save' in i:
                                self.d[i].shaking = self.delete
                    except FileNotFoundError:
                        pass
            if self.d['save3'].click((x, y), event):
                if not self.delete:
                    if not self.d['save3'].save:
                        self.val.save_l = self.d['save3'].savename
                        a = ChoosePlayer(self.menuu, self.val, 'save3')
                        a.run()
                    else:
                        self.val.save_l = self.d['save3'].savename
                        self.val.name = self.d['save3'].pseudo
                        gamee = game.Game((self.val.screensize[0], self.val.screensize[1], self.val.toggle))
                        gamee.run()
                else:
                    try:
                        self.delete_save("third")
                        self.dico['save3'] = str(False)
                        self.save()
                        self.load()
                        for i in self.d.keys():
                            if 'save' in i:
                                self.d[i].shaking = self.delete
                    except FileNotFoundError:
                        pass

    def save(self):
        set = open("Basesave/save.txt", "w")
        set.write("Lastsave: " + str(self.dico['Lastsave']) + "\n")
        set.write("save1: " + str(self.dico['save1']) + "\n")
        set.write("save2: " + str(self.dico['save2']) + "\n")
        set.write("save3: " + str(self.dico['save3']) + "\n")
        set.close()

    def load(self):
        try:
            set = open("Basesave/save.txt", "r")
        except FileNotFoundError:
            set = open("Basesave/save.txt", "w")
            set.close()
            self.load()
        L = set.readlines()

        if len(L) < 4:
            self.dico = {"Lastsave": None, "save1": False, "save2": False, 'save3': False}
        else:
            self.dico = {"Lastsave": ast.literal_eval(L[0].split(": ")[1]),
                         "save1": ast.literal_eval(L[1].split(": ")[1]), "save2": ast.literal_eval(L[2].split(": ")[1]),
                         'save3': ast.literal_eval(L[3].split(": ")[1])}

        self.val.screensize2(self.val.screensize, self.game.screen, self.val.toggle)

        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png', 40, self.val.screensize[1] - 60, 50, 50)
        self.d['SaveTxt'] = PG.Texte('Les sauvegardes : ', self.val.screensize[0] / 2, 30 * self.val.facteur, True,
                                     (255, 255, 255), 32, "../font/Like Snow.otf")
        self.d['save1'] = carte("first", 132 * self.val.facteur, 150 * self.val.facteur, self.dico['save1'])
        self.d['save2'] = carte("second", 514 * self.val.facteur, 150 * self.val.facteur, self.dico['save2'])
        self.d['save3'] = carte("third", 896 * self.val.facteur, 150 * self.val.facteur, self.dico['save3'])

        self.image_fond = PG.img('../img/menu/Fond_Menu.png', 0, 0, self.val.screensize[0], self.val.screensize[1],
                                 False)

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            if i != "TextName":
                self.d[i].iblit(screen)

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
        self.texte = name + ' : ' + str(keys).upper()
        self.txt = PG.Texte(self.texte, x, y, False, (255, 255, 255), 32, '../font/Like Snow.otf')
        self.stats = False

    def change_stats(self, boole):
        """
        Il change les statistiques du Texte

        :param boole: une valeur booléenne, Vrai ou Faux
        """
        self.stats = boole
        if self.stats:
            self.txt = PG.Texte(self.texte, self.x, self.y, False, (255, 0, 255), 32, '../font/Like Snow.otf')
        else:
            self.txt = PG.Texte(self.texte, self.x, self.y, False, (255, 255, 255), 32, '../font/Like Snow.otf')

    def click(self, mousepos, event):
        return self.txt.click(mousepos, event)

    def change(self, keys):
        self.texte = self.name + ' : ' + str(keys).upper()
        self.txt = PG.Texte(self.texte, self.x, self.y, False, (255, 255, 255), 32, '../font/Like Snow.otf')

    def iblit(self, screen):
        self.txt.iblit(screen)


class carte():
    def __init__(self, savename, x, y, Save_exist=False):
        """
        Il prend une chaîne et renvoie une liste des mots de la chaîne, en utilisant une virgule comme chaîne de
        délimitation

        :param savename: le nom du dossier de sauvegarde
        :param x: La coordonnée x du coin supérieur gauche du bouton
        :param y: Coordonnée y du coin supérieur gauche du rectangle
        :param Save_exist: s'il y a une sauvegarde dans le dossier, defaults to False (optional)
        """
        self.save = Save_exist
        self.savename = savename
        self.img = PG.bouton('../img/menu/carte.png', x, y, 250, 500, False)
        self.infos()

        if not self.save:
            self.txt = PG.Texte('No save here', x + 125, y + 250, True)
        else:
            self.txt = PG.Texte(self.pseudo, x + 125, y + 250, True)

        self.shaking = False
        self.image_x = 0

    def infos(self):
        """
        Il lit le fichier sauvegarde.txt et récupère le nom du joueur
        """
        if self.save:
            w = open(self.savename + '/save/sauvegarde.txt', "r")
            L = w.readlines()
            print(self.savename, L[2].split(': ')[1])
            self.pseudo = L[2].split(': ')[1].strip()
            w.close()

    def shake(self, x):
        self.img.shake(x)

    def click(self, mousepos, event):
        """
        Il prend la position de la souris et l'événement, puis il imprime le résultat de la fonction de clic de l'image

        :param mousepos: La position de la souris sur l'écran
        :param event: L'événement qui a été déclenché
        :return: La valeur de retour est la valeur de la fonction click de l'objet image.
        """
        return self.img.click(mousepos, event)

    def iblit(self, screen):
        """
        Il prend un objet d'écran et blit les objets d'image et de texte vers celui-ci

        :param screen: L'écran sur lequel blit
        """
        self.image_x += 0.1
        if self.shaking:
            self.shake(self.image_x)
        else:
            self.img.image = self.img.img_copy
        self.img.iblit(screen)
        self.txt.iblit(screen)


Menu = menu(valeurs.valeur)
Menu.run()
