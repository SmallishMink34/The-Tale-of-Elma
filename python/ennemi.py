import pygame
import pandas as pd
import random as rd


class mob():
    def __init__(self, id, lvlmob):
        self.id = id
        self.lvlmob = lvlmob 
        self.tilesize = 150
        self.tilesizescale = 1
        self.read()
        self.sprite = pygame.image.load(self.img).convert_alpha()
        
        
    def read(self):
        # Fonction qui permet de récupérer les stats des entitées dans notre fichier CSV "MobsStats"
        MobStat = pd.read_csv("../python/info/MobsStats.csv",sep =";", low_memory= False)
        info = MobStat.loc[self.id-1, ["ID","Nom","type","Pvmin","Pvmax","Atkmin","Atkmax","Defmin","Defmax","Speedmin","Speedmax","Img"]]
        self.Nom = info["Nom"]
        self.type = info["type"]
        self.Pv = round(rd.randint(info["Pvmin"], info["Pvmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.PvMax = self.Pv
        self.Atk = round(rd.uniform(info["Atkmin"],info["Atkmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.Def = round(rd.randint(info["Defmin"],info["Defmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.Speed = round(rd.randint(info["Speedmin"],info["Speedmax"]),2) * (self.lvlmob * 0.5 + 1)
        self.img = info["Img"]

        
    def imgload(self, facteur):
    # image du mob pdt le fight 

        self.mobimg = pygame.image.load(self.img).convert_alpha()
        self.mobimg = pygame.transform.scale(self.mobimg, (int(self.mobimg.get_size()[0]*2*facteur), int(self.mobimg.get_size()[1]*2*facteur)))
        self.mobimg = pygame.transform.flip(self.mobimg, 180, 0)
        self.mobimg.set_colorkey((0, 0, 0))
        self.mobimg_rect = self.mobimg.get_rect()
        self.mobimg_rect.centerx = 975*facteur
        self.mobimg_rect.centery = 225*facteur
