import pygame
import ClassPG
import pandas as pd
import random as rd
from PIL import Image, ImageFilter


class fight():
    def __init__(self, joueur, mobid:int, lvlmob:int):
        self.enfight = True
        self.tour = False
        self.joueur = joueur
        self.mobid = mobid
        self.armid = 1
        self.lvlmob = lvlmob
        self.read()
        pygame.init()
        self.size = (1280,720)
        self.defaultsize = (1280, 720)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("FightScreen")
        self.FightScreen()
        
        
        
    def read(self):
        # Fonction qui permet de récupérer les stats des entitées dans notre fichier CSV "MobsStats"
        MobStat = pd.read_csv("../python/info/MobsStats.csv",sep =";", low_memory= False)
        info = MobStat.loc[self.mobid -1 , ["ID","Nom","type","Pvmin","Pvmax","Atkmin","Atkmax","Defmin","Defmax","Speedmin","Speedmax","Img"]]
        self.id = info["ID"]
        self.Nom = info["Nom"]
        self.type = info["type"]
        self.Pv = round(rd.randint(info["Pvmin"], info["Pvmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.Atk = round(rd.uniform(info["Atkmin"],info["Atkmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.Def = round(rd.randint(info["Defmin"],info["Defmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.Speed = round(rd.randint(info["Speedmin"],info["Speedmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.img = info["Img"]
        #Permet de récuperer les stats des armes 
        Armes = pd.read_csv("../python/info/Armes.csv", sep=";", low_memory=False)
        info2 = Armes.loc[self.armid-1, ["ID","Nom","Dmg","img"]]
        self.id2 = info2["ID"]
        self.name = info2["Nom"]
        self.dmg = info2["Dmg"]
        self.imga = info2["img"]
        
        self.realdmg = self.dmg//1.3 - self.Def//4

    # Image de fond
    def image(self, ancien):
        pygame.image.save(ancien, "../img/temp/screen.png")
        image = Image.open("../img/temp/screen.png")
        image = image.filter(ImageFilter.GaussianBlur(radius=4))
        image.save("../img/temp/screen.png")
        
        
    def FightScreen(self):
        running = True
        
        bottom = pygame.image.load("../img/Fight/bas.png").convert_alpha()
        bottom = pygame.transform.scale(bottom,(self.size[0], self.size[1]))
        bottom_rect = bottom.get_rect()
        bottom_rect.x = 0
        bottom_rect.y = self.size[1]//6*0.025
        # Bouton Atk
        
        batk = pygame.image.load("../img/Fight/Attaques.png").convert_alpha()
        batk = pygame.transform.scale(batk, (200*(self.size[0]/self.defaultsize[0]),100*(self.size[1]/self.defaultsize[1])))
        batk_rect = batk.get_rect()
        batk_rect.centerx = self.size[0]//6*1.5
        batk_rect.centery =  self.size[1]//5*4
        
        # Bouton Objets
        
        bobj = pygame.image.load("../img/Fight/Objets.png").convert_alpha()
        bobj = pygame.transform.scale(bobj, (200*(self.size[0]/self.defaultsize[0]),100*(self.size[1]/self.defaultsize[1])))
        bobj_rect = bobj.get_rect()
        bobj_rect.centerx = self.size[0]//6*3
        bobj_rect.centery = self.size[1]//5*4
        
        # Bouton Escp
        
        bf = pygame.image.load("../img/Fight/Fuir.png").convert_alpha()
        bf = pygame.transform.scale(bf, (200*(self.size[0]/self.defaultsize[0]),100*(self.size[1]/self.defaultsize[1])))
        bf_rect = bf.get_rect()
        bf_rect.centerx = self.size[0]//6*4.5
        bf_rect.centery = self.size[1]//5*4
        
        #Image de fond 
         
        Img = ClassPG.img("../img/temp/screen.png", 0, 0, self.size[0], self.size[1], False)
         
        # Compteur pour le tour par tour 
        
        compteur = 0 
        while running : 
            if not self.enfight: 
                running == False 
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    running = False
                if events.type == pygame.MOUSEBUTTONDOWN and self.tour == True :
                    if events.button == 1: # 1= clique gauche
                        if batk_rect(events.pos):
                            self.Pv -= self.realdmg
                            self.tour = False 
                            if self.Pv <= 0 : 
                                self.enfight == False
                        if bf_rect(events.pos):
                            self.enfight == False
            if self.tour == False:
                compteur +=1
                if compteur == 200 :
                    self.joueur.hp -= self.Atk//1.3 - self.joueur.deffence//4
                    if self.joueur.hp <= 0:
                        self.enfight == False
                elif compteur == 400:
                    compteur == 0
                    self.tour == True 
                
            Img.iblit(self.screen)
            self.screen.blit(bottom, bottom_rect)
            self.screen.blit(bf, bf_rect)

            pygame.display.update()
            self.screen.blit(batk, batk_rect)
            self.screen.blit(bobj,bobj_rect)