import pygame
import inv
import ClassPG, pygame_textbox
from valeurs import valeur


class Gui:
    def __init__(self, name, player, size=(1280, 720)):
        self.name = name
        self.player = player

        self.w = size[0]
        self.h = size[1]

        self.facteur = self.w/1280

        self.element = {}
        self.InGame()


        self.currentGui = 'InGame'

        self.move = None
        self.sep = None

    def Game(self, name):
        pass

    def InGame(self):
        self.currentGui = "InGame"
        self.element = {}
        self.element['Pname'] = [ClassPG.Texte(self.player.name, 20, 20, False, (255, 255, 255), 32), True]
        self.element['Kaction'] = [ClassPG.Texte("Interagir : "+str(pygame.key.name(valeur.l["interact"])).upper(), self.w/2, self.h-30, True, (255, 255, 255), int(15*self.facteur)),
                                   self.player.KeyAction]

    def DialogB(self, name, texte):
        self.currentGui = "DialogB"
        self.element = {}
        self.element['Dialog'] = [ClassPG.img('../img/Dialog/GrosseBoite.png', 0, 0, self.w, self.h, False), True]
        self.element['name'] = [ClassPG.Texte(name, self.w/10, self.h/10, False, (0, 0, 0), 32), True]
        self.element['texte'] = [pygame_textbox.textealign(texte, ('Arial', int(32*self.facteur)), (self.w/2, self.h/2), (0, 0, 0)), True]
        self.element['cross'] = [ClassPG.bouton('../img/imgbutton/cross.png', self.w-80, 50, 80, 80), True]
        self.player.allinputoff(False)

    def DialogP(self, name, texte):
        self.currentGui = "DialogP"
        self.element = {}
        self.element['Dialog'] = [ClassPG.img('../img/Dialog/PetiteBoite2.png', 0, 0, self.w, self.h, False), True]
        self.element['name'] = [ClassPG.Texte(name, 110*self.facteur, (455*self.facteur), False, (0, 0, 0), int(32*self.facteur)), True]
        self.element['texte'] = [pygame_textbox.textealign(texte, ('Arial', int(32*self.facteur)), (640*self.facteur, 500*self.facteur), (0, 0, 0)), True]
        self.element['cross'] = [ClassPG.bouton('../img/imgbutton/cross.png', self.w-80, 50, 80, 80), True]
        self.player.allinputoff(False)

    def Mind(self, texte):
        self.currentGui = "Mind"
        self.element = {}
        self.element['Dialog'] = [ClassPG.img('../img/Dialog/Mind.png', 0, 0, self.w, self.h, False), True]
        self.element['texte'] = [pygame_textbox.textealign(texte, ('Arial', int(32*self.facteur)), (640*self.facteur, 500*self.facteur), (255, 255, 255)), True]
        self.player.allinputoff(False)

    def inventory(self, inv):
        self.currentGui = "Inv"
        self.element['inv'] = [inv, True]
        print('Inventaire Ouvert')
        self.element['inv'][0].load_inv()
        self.element['money'] = [ClassPG.Texte(str(self.player.money), 845*self.facteur, 110*self.facteur, True), True]
        self.player.allinputoff(False)

    def inventory_chest(self, name):
        self.currentGui = "Invc"
        self.element['inv'] = [inv.invdouble("c", "p", name, self.player.screen.get_size()), True]
        self.element['inv'][0].load_inv()
        print(f'{name} Ouvert')
        self.player.allinputoff(False)

    def Carte(self, stade:int):
        self.currentGui = "Carte"
        self.element["Carte"] = [ClassPG.img(f"../img/Carte/Carte_{str(stade)}.jpg", 10, 10, 1260*self.facteur, 700*self.facteur, False), True]
        self.player.allinputoff(False)

    def buy(self, item, map):
        self.currentGui = "Buy"
        self.oldmap = map
        self.item = item
        self.element['texte'] = [ClassPG.Texte("Voulez vous achetez "+str(item.name)+" ?", 640*self.facteur, 300*self.facteur, True), True]
        self.element['texte2'] = [
            ClassPG.Texte("Prix : " + str(item.properties['money']) + " $", 640 * self.facteur, 340 * self.facteur, True),
            True]
        self.element["Valider"] = [ClassPG.Texte("Valider", 690*self.facteur, 380*self.facteur, True), True]
        self.element["Annulerr"] = [ClassPG.Texte("Annuler", 590 * self.facteur, 380 * self.facteur, True), True]
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

    def close(self):
        self.InGame()
        self.player.allinputoff(True)

    def event(self, mousepos, event):

        if self.currentGui == "DialogB" or self.currentGui == "DialogP":
            if self.element['cross'][0].click(mousepos, event) or self.player.pressed.get(pygame.K_ESCAPE):
                self.close()

        if self.player.pressed.get(pygame.K_ESCAPE):
            if self.currentGui == "Inv":
                self.element['inv'][0].save("player")
            self.close()

        if self.currentGui == "Inv" or self.currentGui == "Invc":
            # self.element['inv'][0].info_case(mousepos, event)
            if self.move:
                self.element['inv'][0].image_suivie(self.c, mousepos)
            if self.sep :
                self.element['inv'][0].image_suivie(self.c, mousepos)
            LEFT = 1
            RIGHT = 3
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                self.move = True
                self.c = self.element['inv'][0].hover(mousepos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                self.move = False
                self.c2 = self.element['inv'][0].hover(mousepos)
                if not self.c2:
                    self.c2 = self.c
                self.element["inv"][0].move(self.c, self.c2)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            #     objet = inv.item(10, 1)
                objet2 = inv.item(27, 1)
            #     self.element['inv'][0].add(objet, "c1")
                self.element['inv'][0].add(objet2, "c10")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                self.sep = True
                self.c = self.element['inv'][0].hover(mousepos)

                # self.c = self   .element['inv'][0].hover(mousepos)
                # obj = self.element['inv'][0].separateur(self.c)
                # self.element['inv'][0].image_suivie(self.c, mousepos)
                # self.element['inv'][0].add(obj, self.c)

            if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
                self.sep = False
                self.c2 = self.element['inv'][0].hover(mousepos)
                if not self.c2:
                    self.c2 = self.c
                self.element["inv"][0].move_sep(self.c, self.c2)

        if self.currentGui == "Buy":
            if self.element['Valider'][0].click(mousepos, event):
                self.oldmap.buy(self.item)
                self.close()
            elif self.element["Annulerr"][0].click(mousepos, event):
                self.close()