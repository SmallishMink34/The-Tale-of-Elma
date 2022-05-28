import pygame
import pandas as pd
import ClassPG as PG
import ennemi

class Ennemy(pygame.sprite.Sprite):
    def __init__(self, id, lvl, x, y):
        super().__init__()
        self.id = id
        self.lvl = lvl
        self.x, self.y = x, y
        self.w, self.h = 40, 40
        self.recupinfo()
        self.texte = PG.Texte(str(self.lvl), x, y-self.w/2, True)

        mob = ennemi.mob(self.id, self.lvl)
        mob.imgload(1)

        self.type = "entity"
        self.image = pygame.image.load(self.imglink).convert_alpha()
        hauteur = self.image.get_size()[1] / self.image.get_size()[0]
        self.h *= hauteur
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.w, self.rect.h = self.w, self.h
        self.rect.centerx, self.rect.centery = self.x, self.y

    def recupinfo(self):
        """
        Il lit un fichier csv et récupère les informations du mob
        """
        data = pd.read_csv(r'info/MobsStats.csv', sep=';', low_memory=False)
        info = data.loc[self.id-1, ["ID","Nom","type" ,"Img"]]
        self.nom = str(info["Nom"])

        self.imglink = str(info["Img"])

class Ennemis_Txt:
    def __init__(self, texte):
        pass