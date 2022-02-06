import pygame
import pygame
import ClassPG as pg
from pygame.locals import *

class case:
    def __init__(self,coord,obj=None):
        self.coord = coord
        self.img = pg.img("../img/img.inv/case.png", self.coord[0], self.coord[1], 80, 80,False)
        self.rect = self.img.get_recte()
        self.obj = obj
        
    def __str__(self):
        if self.obj != None:
            return str([self.obj.nom,self.obj.nbr])
        else:
            return "la case est vide"
        
    def add_obj(self,obj):
        if self.obj != None:
            if self.obj.id == obj.id:
                self.add_nb(obj.nbr)
            else:
                self.obj = obj
                self.obj.update_coord((self.rect.centerx,self.rect.centery))
        else:
            self.obj = obj
            self.obj.update_coord((self.rect.centerx,self.rect.centery))
        self.obj.update_txt((self.rect.centerx,self.rect.centery))
        
        
    def supr_obj(self):
        self.obj = None
    
    
    def iblit(self,screen):
        screen.blit(self.img.image,self.rect)
        if self.obj != None:
            self.obj.iblit(screen)
    
    def add_nb(self,nbr):
        self.obj.nbr += nbr
        self.obj.update_txt((self.rect.centerx,self.rect.centery))
        
            
            



class inv:
    def __init__(self, text: str, personnage: str,inv:str,name:str):
        """[class pour l'inventaire]
        Args:
            text (str): [le texte que l'on veut afficher au dessus du personnage dans l'inventaire]
            personnage (str): [lien de l'image en png du personnage]
        """
        self.text = pg.Texte(text, 500, 175, True, size=80, color=(0, 0, 0))
        self.personnage = pg.img(personnage, 540, 360, 230, 230, True)
        self.type = inv
        self.name = name
        # On crée un dictionnaire qui gère l'integraliter de l'inventaire
        self.c = self.lire_inv(f"inv.case/{inv}.txt")
        self.save(self.type)
    def iblit(self, screen):
        """[Methode qui blit tout ce qu'il a afficher]"""
        if self.type == "inv":
            self.text.iblit(screen)  # on blit deja le texte
            self.personnage.iblit(screen)  # on blit le personnage
        pg.img("../img/img.inv/INV.png", 0, 0, 1280, 720, False).iblit(screen)  # on blit deja le fond

        for c in self.c.keys():  # on blit toute les cases
            self.c[c].iblit(screen)

    def lire_inv(self,file):
        self.file = open(file,"r")
        L = self.file.readlines()
        c = {}
        for i in L:
            c[i.split(":")[0]] = case((float((i.split(":")[1].split(",")[0]).strip()),float((i.split(":")[1].split(",")[1].strip()))))
        return c
    
    def save(self,name):
        file = open(f"save.inv/{name}.txt","w")
        for c in self.c.keys():
            if self.c[c].obj != None:
                file.write((str(c) + ": ")+str(self.c[c].obj.recup())+"\n")
            else:
                file.write((str(c) + ": ")+str(None)+"\n")
        
    def import_save(self,name):
        
    
    def add(self, obj, case):
        """[Méthode qui ajoute un objet à l'inv]"""
        self.c["c"+str(case)].add_obj(obj)  

    def suppr(self, case):
        """[Méthode qui suprime l'item dans la case de l'inv]"""
        self.c["c"+str(case)].supr_obj()

    def clear(self):
        """[Méthode qui vide l'inv]"""
        for i in range(1, 21):
            self.suppr(i)

    def image_suivie(self, case, mouse_pos):
        """[Methode qui permet de faire suivre l'image sur le curseur]

        Args:
            case (str): [la case dans la quelle il y'a l'image que l'on veut déplacer]
            mouse_pos : [la position du curseur de souris]
        """
        c = "c"+str(case)
        if c in self.c.keys():
            if self.c[c].obj != None:
                self.c[c].obj.rect.centerx = mouse_pos[0]
                self.c[c].obj.rect.centery = mouse_pos[1]
                self.c[c].obj.update_txt((mouse_pos[0],mouse_pos[1]))
        

    def quelle_case(self, event):
        """[Méthode qui permet de renvoyer le nom de la case sur la quelle on click]

        Returns:
            (str): [le nom de la case] (ex:"c2")
        """
        for i in range(1, 21):
            if self.click(event, i):
                return (i)
        return False

    def hover(self, mouse_pos):
        for i in self.c.keys():
            if self.c[i].rect.collidepoint(mouse_pos):
                return i.replace("c","")
        return False

    def click(self, event, case: str):
        """[Méthode qui permet de renvoyer si on click sur un casse]
        Args:
            case (str): [nom de la case]
        Returns:
            (bool): [renvoie true si on clique sur case]
        """
        if "c"+str(case) in self.c.keys():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.c["c"+str(case)].rect.collidepoint(event.pos):
                    return True
            else:
                return False

    def move(self, case1: int, case2: int):
        
        if "c"+str(case1) in self.c.keys():
            if self.c["c"+str(case1)].obj == None: # si on déplace un None
                return False
            elif case1 == case2: # si c'est la meme case
                # self.c["c"+str(case1)].obj.rect.centerx , self.c["c"+str(case1)].obj.rect.centery = self.c["c"+str(case1)].rect.centerx, self.c["c"+str(case1)].rect.centery
                self.c["c"+str(case1)].obj.update_coord((self.c["c"+str(case1)].rect.centerx, self.c["c"+str(case1)].rect.centery))
            elif self.c["c"+str(case2)].obj == None: # si la deuxieme case est vide
                self.add(self.c["c"+str(case1)].obj,case2)
                self.suppr(case1)
            elif self.c["c"+str(case1)].obj.id ==  self.c["c"+str(case2)].obj.id:
                self.c["c"+str(case2)].add_nb(self.c["c"+str(case1)].obj.nbr)
                self.suppr(case1)
            elif self.c["c"+str(case2)].obj != None: # si la deuxieme case n'est pas vide
                c1 = self.c["c"+str(case1)].obj
                c2 = self.c["c"+str(case2)].obj
                self.add(c2,case1)
                self.add(c1,case2)
        self.save(self.name)


    def info_case(self,mouse_pos,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for i in self.c.keys():
                if self.c[i].rect.collidepoint(mouse_pos):
                    print(self.c[i])
           


class item:
    def __init__(self, ID:int , nom: str, nbr: int, genre: str, img: str,coord:tuple = (0,0), nbr_max:int = 64):
        """
        [class permettant de crée un objet]

        Args:
            nom (str): [le nom de l'objet]
            nbr_max (int): [le nombre d'objet à empiler maximum]
            genre (str): [le genre d'objet par (ex "armure")]
            img (str): [le lien de l'image]
            pos_inv (optional): [on precise la position de l'objet dans l'inventaire]. Defaults to None.
        """
        self.id = ID
        self.nom = nom
        self.nbr = nbr
        self.nbr_max = nbr_max
        self.genre = genre
        self.img = pg.img(img,coord[0],coord[1], 80, 80, False)
        self.rect = self.img.get_recte()
        
        self.text = pg.Texte(str(self.nbr),coord[0],coord[1],True)
        
    
    def recup(self):
        return [self.id, self.nom, self.nbr, self.genre, self.nbr_max]
    
    def iblit(self,screen):
        self.img.iblit(screen)
        if self.nbr > 1:
            self.text.iblit(screen)
    
    def update_coord(self,coord):
        self.rect.centerx,self.rect.centery = coord[0],coord[1]
        self.text.updatecoords(coord[0],coord[1])
        
    def update_txt(self,coord):
        self.text.iupdate(self.nbr,(255,255,0),(coord[0],coord[1]))
