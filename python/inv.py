from re import A
import pygame
import pygame
import ClassPG as pg
from pygame.locals import *
import pandas as pd
import ast  # Module transforme representation of list into list


class case:
    def __init__(self, coord, obj=None, casename = "c", casenumber = 0 ):
        self.coord = coord
        self.coord_save = coord
        self.img = pg.img("../img/img.inv/case.png", self.coord[0], self.coord[1], 80, 80, False)
        self.rect = self.img.get_recte()
        self.obj = obj
        self.casename = casename
        self.casenumber = casenumber
        if self.casenumber == "c1":
            self.genre = "casque"
        elif self.casenumber == "c2":
            self.genre = "plastron"
        elif self.casenumber == "c3":
            self.genre = "jambiere"
        elif self.casenumber == "c4":
            self.genre = "botte"
        else :
            self.genre = "None"
            

    def __str__(self):
        if self.obj != None:
            return str([self.obj.nom, self.obj.nbr])
        else:
            return "la case est vide"

    def add_obj(self, obj):
        if self.obj != None:
            if self.obj.id == obj.id :
                self.add_nb(obj.nbr)

            else:
                self.obj = obj
                self.obj.update_coord((self.rect.centerx, self.rect.centery))
        else:
            self.obj = obj
            self.obj.update_coord((self.rect.centerx, self.rect.centery))
        self.obj.update_txt((self.rect.centerx, self.rect.centery))

    def supr_obj(self):
        self.obj = None

    def iblit(self, screen):
        screen.blit(self.img.image, self.rect)
        if self.obj != None:
            self.obj.iblit(screen)

    
    def add_nb(self, nbr):
        self.obj.nbr += nbr
        self.obj.update_txt((self.rect.centerx, self.rect.centery))

    def changecoord(self, x, y):
        print(x)
        self.rect.x = x
        self.rect.y = y
        self.obj.update_coord((self.rect.centerx, self.rect.centery))
        self.obj.update_txt((self.rect.centerx, self.rect.centery))

    def click(self, events, mousepos):
        if events.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mousepos):
                return True

    def suppr_nb(self, nbr):
        self.obj.nbr -= 1
        if self.obj.nbr == 0 :
            self.supr_obj()



class inv:
    def __init__(self, text: str, personnage: str, inv: str, name: str, size: tuple):
        """[class pour l'inventaire]
        Args:
            text (str): [le texte que l'on veut afficher au dessus du personnage dans l'inventaire]
            personnage (str): [lpien de l'image en png du personnage]
        """
        self.facteur = size[0] / 1280
        self.text = pg.Texte(text, 300*self.facteur, 105*self.facteur, True, size=80, color=(255, 255, 255), font="../font/Like Snow.otf")
        self.personnage = pg.img("../img/img.inv/player.png", 540*self.facteur, 360*self.facteur, 230*self.facteur, 230*self.facteur, True)
        self.type = inv
        self.name = name
        # On crée un dictionnaire qui gère l'integraliter de l'inventaire

        self.c = self.lire_inv(f"inv.case/{inv}.txt")
        self.lettre = "c"

    def suppr_nb_obj(self, nbr, case):
        """[Méthode qui ajoute un objet à l'inv]"""
        case = case.replace(self.lettre, "") if isinstance(case, str) else case
        self.c[self.lettre + str(case)].suppr_nb(nbr)
        self.save(self.name)


    def load_inv(self):
        self.c = self.lire_inv(f"inv.case/{self.type}.txt")
        self.import_save(self.name)


    def iblit(self, screen):
        """[Methode qui blit tout ce qu'il a afficher]"""
        pg.img("../img/img.inv/INV.png", 0, 0, 1280*self.facteur, 720*self.facteur, False).iblit(screen)  # on blit deja le fond
        if self.type == "inv":
            self.text.iblit(screen)  # on blit deja le texte
            self.personnage.iblit(screen)  # on blit le personnage
        

        for c in self.c.keys():  # on blit toute les cases
            self.c[c].iblit(screen)

    def lire_inv(self, file):
        self.file = open(file, "r")
        L = self.file.readlines()
        c = {}
        for i in L:
            c[i.split(":")[0]] = case(
                (float((i.split(":")[1].split(",")[0]).strip())*self.facteur, float((i.split(":")[1].split(",")[1].strip()))*self.facteur), None,  'c', i.split(":")[0])
        return c

    def save(self, name):
        file = open(f"save.inv/{name}.txt", "w")
        for c in self.c.keys():
            if self.c[c].obj != None:
                file.write((str(c) + ": ") + str(self.c[c].obj.recup()) + "\n")
            else:
                file.write((str(c) + ": ") + str(None) + "\n")
        file.close()

    def import_save(self, name):
        self.clear()
        try:
            a = open(f"save.inv/{name}.txt", "r")
            for i in a.readlines():
                x = str(i.split(": ")[1])
                x = ast.literal_eval(x)
                if x is not None:
                    id = int(x[0])
                    nb = int(x[2])
                    case = i.split(': ')[0][1:]
                    obj = item(id, nb)
                    self.add(obj, case)
            a.close()
        except FileNotFoundError:
            return False

    def add(self, obj, case):
        """[Méthode qui ajoute un objet à l'inv]"""
        case = case.replace(self.lettre, "")
        self.c[self.lettre + str(case)].add_obj(obj)

    def suppr(self, case):
        """[Méthode qui suprime l'item dans la case de l'inv]"""
        self.c[self.lettre + str(case)].supr_obj()

    def clear(self):
        """[Méthode qui vide l'inv]"""
        for i in self.c.keys():
            self.suppr(int(i[1:]))

    def image_suivie(self, case, mouse_pos):
        """[Methode qui permet de faire suivre l'image sur le curseur]

        Args:
            case (str): [la case dans la quelle il y'a l'image que l'on veut déplacer]
            mouse_pos : [la position du curseur de souris]
        """
        c = self.lettre + str(case)
        if c in self.c.keys():
            if self.c[c].obj != None:
                self.c[c].obj.rect.centerx = mouse_pos[0]
                self.c[c].obj.rect.centery = mouse_pos[1]
                self.c[c].obj.update_txt((mouse_pos[0], mouse_pos[1]))

    def hover(self, mouse_pos):
        for i in self.c.keys():
            if self.c[i].rect.collidepoint(mouse_pos):
                return i.replace(self.lettre, "")
        return False

    def click(self, event, case: str):
        """[Méthode qui permet de renvoyer si on click sur un casse]
        Args:
            case (str): [nom de la case]
        Returns:
            (bool): [renvoie true si on clique sur case]
        """
        if self.lettre + str(case) in self.c.keys():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.c[self.lettre + str(case)].rect.collidepoint(event.pos):
                    return True
            else:
                return False

    def move(self, case1: int, case2: int):

        if self.lettre + str(case1) in self.c.keys():
            if self.c[self.lettre + str(case1)].obj == None:  # si on déplace un None
                return False
            elif case1 == case2:  # si c'est la meme case
                self.c[self.lettre + str(case1)].obj.update_coord(
                    (self.c[self.lettre + str(case1)].rect.centerx, self.c[self.lettre + str(case1)].rect.centery))
            elif self.c[self.lettre + str(case2)].obj is None :  # si la deuxieme case est vide
                if self.c[self.lettre + str(case1)].obj.genre == self.c[self.lettre + str(case2)].genre or self.c[self.lettre + str(case2)].genre == "None": # si les deux genre sont identique ou si la case est vide
                    print("déplacer")
                    self.add(self.c[self.lettre + str(case1)].obj, case2)
                    self.suppr(case1)
                else: # sinon on la remet au meme endroit
                    self.c[self.lettre + str(case1)].obj.update_coord(
                        (self.c[self.lettre + str(case1)].rect.centerx, self.c[self.lettre + str(case1)].rect.centery))
            elif self.c[self.lettre + str(case1)].obj.id == self.c[self.lettre + str(case2)].obj.id:
                if self.c[self.lettre + str(case1)].obj.genre == self.c[self.lettre + str(case2)].genre or self.c[self.lettre + str(case2)].genre == "None" : 
                    print("empliler")
                    self.c[self.lettre + str(case2)].add_nb(self.c[self.lettre + str(case1)].obj.nbr)
                    self.suppr(case1)
                else: # sinon on la remet au meme endroit
                    self.c[self.lettre + str(case1)].obj.update_coord(
                        (self.c[self.lettre + str(case1)].rect.centerx, self.c[self.lettre + str(case1)].rect.centery))
            
            elif self.c[self.lettre + str(case2)].obj is not None:  # si la deuxieme case n'est pas vide
                if self.c[self.lettre + str(case1)].obj.genre == self.c[self.lettre + str(case2)].genre and  self.c[self.lettre + str(case1)].genre == self.c[self.lettre + str(case2)].genre:
                    print("échanger")
                    c1 = self.c[self.lettre + str(case1)].obj
                    c2 = self.c[self.lettre + str(case2)].obj
                    self.add(c2, case1)
                    self.add(c1, case2)
                else:
                    self.c[self.lettre + str(case1)].obj.update_coord(
                            (self.c[self.lettre + str(case1)].rect.centerx, self.c[self.lettre + str(case1)].rect.centery))
        self.save(self.name)

    def info_case(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for i in self.c.keys():
                if self.c[i].rect.collidepoint(mouse_pos):
                    print(self.c[i])


class invdouble:
    def __init__(self, case1, playercase, name, size):
        self.case1 = case1
        self.playercase = playercase
        self.name = name
        self.size = size

        self.facteur = self.size[0]/1280

        if "Chest" in name:
            self.allcase = self.lire_inv(f"inv.case/chest.txt")
        else:
            self.allcase = self.lire_inv(f"inv.case/{name}.txt")

    def load_inv(self):
        self.import_save(self.name)

    def iblit(self, screen):
        
        pg.img("../img/img.inv/INV.png", 0, 0, self.size[0], self.size[1], False).iblit(screen)
        for c in self.allcase.keys():  # on blit toute les cases
            self.allcase[c].iblit(screen)
        

        

    def lire_inv(self, file):
        self.file = open(file, "r")
        L = self.file.readlines()
        c = {}
        for i in L:
            c[i.split(":")[0]] = case(
                (float((i.split(":")[1].split(",")[0]).strip())*self.facteur, float((i.split(":")[1].split(",")[1].strip()))*self.facteur), None,str((i.split(":")[0].split(",")[0]).strip())[0])
        return c

    def save(self, name):
        file = open(f"save.inv/{name}.txt", "w")
        file2 = open("save.inv/player.txt", "r")
        lines = file2.readlines()
        file2.close()

        file3 = open("save.inv/player.txt", "w")

        for c in self.allcase.keys():
            if self.case1 in c:
                if self.allcase[c].obj != None:
                    file.write((str(c) + ": ") + str(self.allcase[c].obj.recup()) + "\n")
                else:
                    file.write((str(c) + ": ") + str(None) + "\n")

        for c in lines:
            a = c.split(': ')[0]  # Recup de la clé
            a = a.replace('c', self.playercase)
            if a in self.allcase.keys():
                if self.allcase[a].obj != None:
                    file3.write((str(a) + ": ") + str(self.allcase[a].obj.recup()) + "\n")
                else:
                    file3.write((str(a) + ": ") + str(None) + "\n")
            else:
                file3.write(c)

        file.close()

        file3.close()



    def import_save(self, name):
        self.clear()
        try:
            print('import normal')
            a = open(f"save.inv/{name}.txt", "r")
            for i in a.readlines():
                x = str(i.split(": ")[1])
                x = ast.literal_eval(x) #Resultat (ex: None)
                if x is not None:
                    id = int(x[0])
                    nb = int(x[2])
                    case = i.split(': ')[0][0:] #i = case (ex: c1)
                    if self.playercase not in case:
                        obj = item(id, nb)
                        self.add(obj, case)
            a.close()

            a2 = open(f"save.inv/player.txt", "r")

            for i in a2.readlines():
                x = str(i.split(": ")[1])
                x = ast.literal_eval(x) #Resultat (ex: None)
                if x is not None:
                    id = int(x[0])
                    nb = int(x[2])
                    case = i.split(': ')[0][0:] #i = case (ex: c1)
                    if self.playercase + case[1:] in self.allcase.keys():
                        case = self.playercase + case[1:]
                        obj = item(id, nb)
                        self.add(obj, case)
            a.close()

        except FileNotFoundError:
            self.save(self.name)
            self.import_save(self.name)



    def add(self, obj, case):
        """[Méthode qui ajoute un objet à l'inv]"""
        self.allcase[case].add_obj(obj)

    def suppr(self, case):
        """[Méthode qui suprime l'item dans la case de l'inv]"""
        self.allcase[str(case)].supr_obj()

    def clear(self):
        """[Méthode qui vide l'inv]"""
        for i in self.allcase.keys():
            self.suppr(i)

    def image_suivie(self, case, mouse_pos):
        """[Methode qui permet de faire suivre l'image sur le curseur]

        Args:
            case (str): [la case dans la quelle il y'a l'image que l'on veut déplacer]
            mouse_pos : [la position du curseur de souris]
        """
        c = str(case)
        if c in self.allcase.keys():
            if self.allcase[c].obj is not None:
                self.allcase[c].obj.rect.centerx = mouse_pos[0]
                self.allcase[c].obj.rect.centery = mouse_pos[1]
                self.allcase[c].obj.update_txt((mouse_pos[0], mouse_pos[1]))

    def hover(self, mouse_pos):
        for i in self.allcase.keys():
            if self.allcase[i].rect.collidepoint(mouse_pos):
                return i
        return False

    def click(self, event, case: str, lettre:str='c'):
        """[Méthode qui permet de renvoyer si on click sur un casse]
        Args:
            case (str): [nom de la case]
        Returns:
            (bool): [renvoie true si on clique sur case]
        """
        if lettre + str(case) in self.allcase.keys():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.allcase[lettre + str(case)].rect.collidepoint(event.pos):
                    return True
            else:
                return False

    def move(self, case1: int, case2: int):
        if str(case1) in self.allcase.keys():
            if self.allcase[str(case1)].obj == None:  # si on déplace un None
                return False
            elif case1 == case2:  # si c'est la meme case
                self.allcase[str(case1)].obj.update_coord(
                    (self.allcase[str(case1)].rect.centerx, self.allcase[str(case1)].rect.centery))
            elif self.allcase[str(case2)].obj is None:  # si la deuxieme case est vide
                self.add(self.allcase[str(case1)].obj, case2)
                self.suppr(case1)
            elif self.allcase[str(case1)].obj.id == self.allcase[str(case2)].obj.id:
                self.allcase[str(case2)].add_nb(self.allcase[str(case1)].obj.nbr)
                self.suppr(case1)
            elif self.allcase[str(case2)].obj is not None:  # si la deuxieme case n'est pas vide
                c1 = self.allcase[str(case1)].obj
                c2 = self.allcase[str(case2)].obj
                self.add(c2, case1)
                self.add(c1, case2)
        self.save(self.name)

    def info_case(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for i in self.allcase.keys():
                if self.allcase[i].rect.collidepoint(mouse_pos):
                    print(self.allcase[i])

class item:
    def __init__(self, ID: int, nb: int, coord: tuple = (0, 0)):
        """
        [class permettant de crée un objet]

        Args:
            nom (str): [le nom de l'objet]
            nbr_max (int): [le nombre d'objet à empiler maximum]
            genre (str): [le genre d'objet par (ex "p")]
            img (str): [le lien de l'image]
        """
        self.id = ID
        self.nbr = nb
        self.recupinfoitem()

        self.img = pg.img(self.imglink, coord[0], coord[1], 80, 80, False)

        self.rect = self.img.get_recte()
        self.text = pg.Texte(str(self.nbr), coord[0], coord[1], True)

    def recupinfoitem(self):
        data = pd.read_csv(r'info/items.csv', sep=',', low_memory=False)
        info = data.loc[self.id - 1, ["Id", "name", "type", "imglink", "nbmax", "link"]]
        self.nom = str(info["name"])
        self.genre = str(info["type"])
        print(info["type"])
        self.imglink = str(info["imglink"])
        self.nbr_max = int(info["nbmax"])   
        self.link = int(info["link"])

    def recup(self):
        return [self.id, self.nom, self.nbr, self.genre, self.nbr_max]

    def iblit(self, screen):
        self.img.iblit(screen)
        if self.nbr > 1:
            self.text.iblit(screen)

    def update_coord(self, coord):
        self.rect.centerx, self.rect.centery = coord[0], coord[1]
        self.text.updatecoords(coord[0], coord[1])

    def update_txt(self, coord):
        self.text.iupdate(self.nbr, (255, 255, 0), (coord[0], coord[1]))
