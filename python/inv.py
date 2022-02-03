import pygame
import pygame
import ClassPG as pg
from pygame.locals import *
import game

class inv:
    def __init__(self,text:str,personnage:str):
        """[class pour l'inventaire]
        Args:
            text (str): [le texte que l'on veut afficher au dessus du personnage dans l'inventaire]
            personnage (str): [lien de l'image en png du personnage]
        """
        self.text = pg.Texte(text,500,175,True,size = 80,color=(0,0,0))
        self.personnage = pg.img(personnage,540,360,230,230,True)
        
        # On crée un dictionnaire qui gère l'integraliter de l'inventaire
        self.c = {'c1': [(312.82,235.37)], 'c2': [(312.82,320,31)], 'c3': [(312.82,404.87)], 'c4': [(312.82,489.68)], 'c5': [(571.73,489.68)], 'c6': [(718.75,150.79)], 'c7': [(803.19,150.85)], 'c8': [(887.72,150.92)], 'c9': [(718.75,235.73)], 'c10': [(803.19,235.79)], 'c11': [(887.72,235.85)], 'c12': [(718.75,320.29)], 'c13': [(803.19,320.35)], 'c14': [(887.72,320.42)], 'c15': [(718.75,405.1)], 'c16': [(803.19,405.25)], 'c17': [(887.72,404.87)], 'c18': [(718.75,489.7)], 'c19': [(803.19,489.76)], 'c20': [(887.72,489.82)], 'c21' : [(333,235)]}
        for i in range(1,21):
            c = "c"+str(i)
            self.c[c].append(self.c[c][0]) # on fait une sauvegarde de coord
            self.c[c].append(pg.img("img/img.inv/case.png",self.c[c][0][0],self.c[c][0][1],80,80,False)) # on definie les petits carrés noir
            self.c[c].append(self.c[c][2].take_rect()) # on crée le rect des carrés noir
            self.c[c].append(None) # pas d'image dans la case
            self.c[c].append(None) # pas d'image dans la case
        
    def iblit(self,screen):
        """[Methode qui blit tout ce qu'il a afficher]"""
        self.text.iblit(screen) # on blit deja le texte
        pg.img("img/img.inv/INV.png",0,0,1280, 720,False).iblit(screen) # on blit deja le fond
        self.personnage.iblit(screen) # on blit le personnage
        for i in range(1,21): # on blit toute les cases
            c = "c"+str(i)
            self.c[c][2].iblit(screen)
            if self.c[c][4] != None: # si il y'a une image
                self.c[c][5].iblit(screen)# on blit l'image    
        
    def add(self,obj):
        """[Méthode qui ajoute un objet à l'inv]"""
        c = obj[4]
        self.c[c][4] = obj
        self.c[c][5] = pg.img(self.c[c][4][3],self.c[c][1][0],self.c[c][1][1],80,80,False)

    def suppr(self,case):
        """[Méthode qui suprime l'item dans la case de l'inv]"""
        self.c[case][4] = None # on suprime l'image
        self.c[case][5] = None # on suprime le lien de l'image
    
    def clear(self):
        """[Méthode qui vide l'inv]"""
        for i in range(1,21):
            self.c["c"+str(i)][4]=None
            
    def image_suivie(self,case,mouse_pos):
        """[Methode qui permet de faire suivre l'image sur le curseur]

        Args:
            case (str): [la case dans la quelle il y'a l'image que l'on veut déplacer]
            mouse_pos : [la position du curseur de souris]
        """
        if self.c[case][4] != None:
            self.c[case][0] = mouse_pos
            self.c[case][5] = pg.img(self.c[case][4][3],self.c[case][0][0],self.c[case][0][1],80,80,True)
    
    def quelle_case(self,event):
        """[Méthode qui permet de renvoyer le nom de la case sur la quelle on click]

        Returns:
            (str): [le nom de la case] (ex:"c2")
        """
        for i in range(1,21):
            if self.click(event, 'c'+str(i)):
                return('c'+str(i))
        return False
        
    def click(self,event,case:str):
        """[Méthode qui permet de renvoyer si on click sur un casse]
        Args:
            case (str): [nom de la case]
        Returns:
            (bool): [renvoie true si on clique sur case]
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.c[case][3].collidepoint(event.pos):
                return True
        else:
            return False
    
    def move(self,case1:str,case2:str):
        """[Méthode qui permet de déplacer une image dans une case]

        Args:
            case1 (str): [nom de la case que l'on veut déplacer]
            case2 (str): [nom de la case ou on veut mettre case 1]
        """
        if self.c[case1][4] == None: 
            return False
        if case1 == case2:
            self.c[case2][5] = pg.img(self.c[case2][4][3],self.c[case2][1][0],self.c[case2][1][1],80,80,False)
        if self.c[case2][4] != None: 
            self.c[case1][5] = pg.img(self.c[case1][4][3],self.c[case1][1][0],self.c[case1][1][1],80,80,False)
        elif case1 != case2:
            self.c[case2][4],self.c[case2][5] = self.c[case1][4],self.c[case1][5]
            self.c[case2][5] = pg.img(self.c[case2][4][3],self.c[case2][1][0],self.c[case2][1][1],80,80,False)
            self.suppr(case1)
        

class objet:
    def __init__(self,nom,nbr_max,genre,img,pos_inv = None):
        self.nom = nom
        self.nbr_max = nbr_max
        self.genre = genre
        self.img = img
        self.pos_inv = pos_inv

    def recup(self):
        return [self.nom,self.nbr_max,self.genre,self.img,self.pos_inv]

if __name__ == '__main__':
    game.run()