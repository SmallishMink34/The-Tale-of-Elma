import pygame
import pygame
import ClassPG as pg
import ClassPlayer
from pygame.locals import *
import sys
import pyscroll
import pytmx

class inv:
    def __init__(self,img,text):
        self.text = pg.Texte(text,500,175,True,size = 80,color=(0,0,0))
        self.img = pg.img(img,640,360,1280,720)
        self.case = {'c1': [(312.82,235.37)], 'c2': [(312.82,320,31)], 'c3': [(312.82,404.87)], 'c4': [(312.82,489.68)], 'c5': [(571.73,489.68)], 'c6': [(718.75,150.79)], 'c7': [(803.19,150.85)], 'c8': [(887.72,150.92)], 'c9': [(718.75,235.73)], 'c10': [(803.19,235.79)], 'c11': [(887.72,235.85)], 'c12': [(718.75,320.29)], 'c13': [(803.19,320.35)], 'c14': [(887.72,320.42)], 'c15': [(718.75,405.1)], 'c16': [(803.19,405.25)], 'c17': [(887.72,404.87)], 'c18': [(718.75,489.7)], 'c19': [(803.19,489.76)], 'c20': [(887.72,489.82)]}
        for i in range(1,21):
            self.case["c"+str(i)].append(None)
            
            
    def iblit(self,screen):
        self.img.iblit(screen)
        self.text.iblit(screen)
        for i in range(1,21):
            if self.case["c"+str(i)][1] != None:
                self.case["c"+str(i)][1].iblit(screen)
    
    def add(self,img,case):
        """[Méthode qui ajoute un objet à l'inv]"""
        for i in range(1,21):
            if "c"+str(i) == case:
                self.case["c"+str(i)][1] = pg.img(img,self.case["c"+str(i)][0][0],self.case["c"+str(i)][0][1],80,80,False)

    def suppr(self,case):
        """[Méthode qui suprime la case dans l'inv]"""
        self.case[case][1] = None
    
    def clear(self):
        """[Méthode qui vide l'inv]"""
        for i in range(1,21):
            self.case["c"+str(i)][1]=None
        

