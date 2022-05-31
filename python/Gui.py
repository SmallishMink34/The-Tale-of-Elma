import pygame
import inv
import ClassPG, pygame_textbox
from valeurs import valeur
import pandas as pd

#
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

        self.img_survole = inv.survole(pygame.mouse.get_pos(), "")
        self.survole = False

    def Game(self, name):
        pass

    def InGame(self):
        self.currentGui = "InGame"
        self.element = {}
        self.element['Pname'] = [ClassPG.Texte(self.player.name, 20*self.facteur, 10*self.facteur, False, (255, 255, 255), 32), True]
        self.element['Kaction'] = [ClassPG.Texte("Interagir : "+str(pygame.key.name(valeur.l["interact"])).upper(), self.w/2, self.h-30, True, (255, 255, 255), int(15*self.facteur)),
                                   self.player.KeyAction]
        self.element['Vie'] = [ClassPG.img("../img/bar/vie/Vie_00100.png", 0, 50*valeur.facteur,valeur.screensize[0]/4, valeur.screensize[1]/4, False), True]

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
        self.element["background"] = [ClassPG.img("../img/img.inv/INV.png", 0, 0, valeur.screensize[0], valeur.screensize[1], False), True]
        self.element['texte'] = [ClassPG.Texte("Voulez vous achetez "+str(item.name)+" ?", 640*self.facteur, 300*self.facteur, True), True]
        self.element['texte2'] = [
            ClassPG.Texte("Prix : " + str(item.properties['money']) + " $", 640 * self.facteur, 340 * self.facteur, True),
            True]
        self.element["Valider"] = [ClassPG.Texte("Valider", 690*self.facteur, 380*self.facteur, True), True]
        self.element["Annulerr"] = [ClassPG.Texte("Annuler", 590 * self.facteur, 380 * self.facteur, True), True]
        self.player.allinputoff(False)

    def shop(self, marchant):
        self.currentGui = "Shop"
        csv = pd.read_csv(f"../python/info/{marchant}.csv", sep=",", low_memory=False)
        long = len(open(f"../python/info/{marchant}.csv", "r").readlines())-1
        dico = {}
        for i in range(long):
            a = csv.loc[i, ["Item", "price"]]
            dico[str(i)] = [a["Item"], a["price"]]

        self.element["background"] = [
            ClassPG.img("../img/img.inv/INV.png", 0, 0, valeur.screensize[0], valeur.screensize[1], False), True]
        x = 640
        y = 150

        for i in dico.keys():
            self.element[str(i)] = [ItemShop(dico[i], x*valeur.facteur, y*valeur.facteur), True]
            y+=80

        self.element["Money_P"] = [ClassPG.Texte(str(self.player.money), 300*self.facteur, 150, False), True]

    def PlayerLife(self, vie):
        if self.player.hp_previous != self.player.hp:
            self.player.hp_previous = self.player.hp
            self.player.hp = vie
            if self.player.hp > self.player.hpmax: self.player.hp = self.player.hpmax
            if self.player.hp < 0: self.player.hp = 0
            vie = (5- len(str(int(self.player.hp))))*"0"+str(int(self.player.hp))

            self.element['Vie'][0].iupdate(f"../img/bar/vie/Vie_{vie}.png", True, True)

    def Pause(self):
        self.currentGui = "Pause"
        pass

    def iblit(self, screen):
        if self.currentGui == "InGame":
            self.PlayerLife(self.player.hp)
            self.element['Kaction'][1] = self.player.KeyAction
        for i in self.element.keys():
            if self.element[i][1]:
                self.element[i][0].iblit(screen)
        if self.survole and self.currentGui == "Inv":
            self.img_survole.iblit(screen)
        else:
            pass

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_8:
                    objet5 = inv.item(5, 1)
                    objet = inv.item(29, 1)
                    objet2 = inv.item(30, 1)
                    objet3 = inv.item(31, 1)
                    objet4 = inv.item(32, 1)

                    objet6 = inv.item(42, 1)
                    objet7 = inv.item(43, 1)
                    objet8 = inv.item(44, 1)
                    objet9 = inv.item(41, 1)
                    objet10 = inv.item(9, 1)

                    self.element['inv'][0].add(objet, "c12")
                    self.element['inv'][0].add(objet2, "c13")
                    self.element['inv'][0].add(objet3, "c14")
                    self.element['inv'][0].add(objet4, "c15")
                    self.element['inv'][0].add(objet5, "c16")
                    self.element['inv'][0].add(objet6, "c6")
                    self.element['inv'][0].add(objet7, "c7")
                    self.element['inv'][0].add(objet8, "c8")
                    self.element['inv'][0].add(objet9, "c9")
                    self.element['inv'][0].add(objet10, "c10")

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

            if self.element["inv"][0].present_sur_une_case(mousepos) and self.element["inv"][0].name == "player":
                pos = self.element["inv"][0].blit_info(mousepos).coord_save
                if self.element["inv"][0].blit_info(pos).obj != None:
                    self.survole = True
                    self.img_survole.update(pos,self.element["inv"][0].blit_info(mousepos).return_info())
                else:
                    self.survole = False

        if self.currentGui == "Buy":
            if self.element['Valider'][0].click(mousepos, event):
                self.oldmap.buy(self.item)
                self.close()
            elif self.element["Annulerr"][0].click(mousepos, event):
                self.close()

        if self.currentGui == "Shop":
            for i in self.element.keys():
                if i in "1234567890":
                    if self.element[i][0].click(mousepos, event):
                        if self.player.money - self.element[i][0].item[1] >= 0:
                            self.player.money -= self.element[i][0].item[1]
                            self.element["Money_P"][0].iupdate(str(self.player.money), (255,255,255))
                            obj = inv.item(self.element[i][0].item[0], 1)
                            self.player.inventaire.add_last(obj)


class ItemShop:
    def __init__(self, item, x, y):
        self.x, self.y = x, y
        self.item = item
        self.read()
        self.img = ClassPG.img(self.imglink, self.x+10, self.y+10, 40, 40, False)
        self.price = ClassPG.Texte(str(self.item[1]), self.x +60, self.y+10, False)
        self.case = ClassPG.bouton("../img/img.inv/caseshop.png", self.x, self.y, 160, 60)
    def read(self):
        id = self.item[0]

        data = pd.read_csv(r'info/items.csv', sep=',', low_memory=False)
        info = data.loc[id - 1, ["Id", "name", "type", "imglink", "nbmax", "link"]]
        self.nom = str(info["name"])
        self.genre = str(info["type"])
        print(info["type"])
        self.imglink = str(info["imglink"])
        self.nbr_max = int(info["nbmax"])
        self.link = int(info["link"])

    def click(self, mousepos, event):
        if self.case.click(mousepos, event):
            return True

    def iblit(self, screen):
        self.case.iblit(screen)
        self.img.iblit(screen)
        self.price.iblit(screen)