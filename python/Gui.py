import pygame

import ClassPG, pygame_textbox

class Gui:
    def __init__(self, name, player):
        self.name = name
        self.player = player

        self.element = {}
        self.InGame()

        self.currentGui = 'InGame'

    def InGame(self):
        self.currentGui = "InGame"
        self.element = {}
        self.element['Pname'] = [ClassPG.Texte(self.player.name, 20, 20, False, (255,255,255), 32), True]
        self.element['Kaction'] = [ClassPG.Texte("Interagir : E", 640, 700, True, (255, 255, 255), 15), self.player.KeyAction]

    def DialogB(self, name, texte):
        self.currentGui = "DialogB"
        self.element = {}
        self.element['Dialog'] = [ClassPG.img('../img/Dialog/GrosseBoite.png', 0, 0, 1280, 720, False), True]
        self.element['name'] = [ClassPG.Texte(name, 70, 42, False, (0,0,0), 32), True]
        self.element['texte'] = [pygame_textbox.textealign(texte, ('Arial', 32), (640, 320), (0, 0, 0)), True]
        self.element['cross'] = [ClassPG.bouton('../img/imgbutton/cross.png', 1200, 50, 80, 80), True]
        self.player.allinputoff(False)

    def DialogP(self, name, texte):
        self.currentGui = "DialogP"
        self.element = {}
        self.element['Dialog'] = [ClassPG.img('../img/Dialog/PetiteBoite2.png', 0, 0, 1280, 720, False), True]
        self.element['name'] = [ClassPG.Texte(name, 110, 460, False, (0, 0, 0), 32), True]
        self.element['texte'] = [pygame_textbox.textealign(texte, ('Arial', 32), (640, 500), (0, 0, 0)), True]
        self.element['cross'] = [ClassPG.bouton('../img/imgbutton/cross.png', 1200, 50, 80, 80), True]
        self.player.allinputoff(False)

    def Pause(self):
        self.currentGui = "Pause"
        pass

    def iblit(self, screen):
        if self.currentGui == "InGame":
            self.element['Kaction'][1] = self.player.KeyAction
        for i in self.element.keys():
            if self.element[i][1]:
                self.element[i][0].iblit(screen)

    def event(self, mousepos,event):
        if self.currentGui == "DialogB" or self.currentGui == "DialogP":
            if self.element['cross'][0].click(mousepos,event) or self.player.pressed.get(pygame.K_ESCAPE):
                self.InGame()
                self.player.allinputoff(True)