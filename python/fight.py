import pygame
import ClassPG
import ennemi
import pandas as pd
import random as rd
from PIL import Image, ImageFilter


class fight():
    def __init__(self, joueur, mobid:int, lvlmob:int):
        self.enfight = True
        self.joueur = joueur
        self.mobid = mobid
        self.gui = False 
        self.dico = {"heal":self.heal}
        self.w = []
        
        try: 
            self.armid = self.joueur.get_item_in_inventory(5).obj.link
        except AttributeError:
            self.armid = 1
        self.lvlmob = lvlmob
        pygame.init()
        self.size = (1280,720)
        self.defaultsize = (1280, 720)
        self.facteur = self.size[0]/self.defaultsize[0]
        self.screen = pygame.display.set_mode(self.size)
        self.read()
        # Pour savoir qui attaque en premier 
        if self.ennemii.Speed > self.joueur.speedfight:
            self.tour = False # False = tour du mob
            print('cest un en false')
        elif self.ennemii.Speed == self.joueur.speedfight:
            self.tour = rd.choice([False, True])
        else : 
            self.tour = True 
        print(self.tour)
        
        pygame.display.set_caption("FightScreen")

    def read(self):
        #Permet de récuperer les stats des armes 
        Armes = pd.read_csv("../python/info/Armes.csv", sep=";", low_memory=False)
        info2 = Armes.loc[self.armid-1, ["ID","Nom","Dmg","img"]]
        self.id2 = info2["ID"]
        self.name = info2["Nom"]
        self.dmg = info2["Dmg"]
        self.imga = info2["img"]

        
        self.ennemii = ennemi.mob(self.mobid, self.lvlmob)
        self.ennemii.imgload(self.facteur)
        self.realdmg = self.dmg//1.3 - self.ennemii.Def/4 # degat que le joueur inflige
        if self.realdmg < 0 :
            self.realdmg == 0
        self.dmgmob = self.ennemii.Atk//1.3 - self.joueur.deffence/4
        if self.dmgmob < 0:
            self.dmgmob = 0

    # Image de fond
    def image(self, ancien):
        pygame.image.save(ancien, "../img/temp/screen.png")
        image = Image.open("../img/temp/screen.png")
        image = image.filter(ImageFilter.GaussianBlur(radius=4))
        image.save("../img/temp/screen.png")

    
    def afficherinv(self): # Affichage obj
        x = 150*self.facteur
        y = 480*self.facteur
        self.w = []
        for i in self.joueur.inventaire.c.keys():
            if self.joueur.get_item_in_inventory(i.replace("c", "")).obj != None:                    
                t = self.joueur.get_item_in_inventory(i.replace("c", "")).obj.genre
                if t in ["potions"]:
                    self.joueur.get_item_in_inventory(i.replace("c", "")).changecoord(x, y)
                    self.w.append(self.joueur.get_item_in_inventory(i.replace("c", ""))) # on recupere la case et l'objet in 
                    y += 100
                    if y > 580*self.facteur:
                        x += 100
                        y = 480*self.facteur
                        
                        
    def potions(self, Id):
        potions2 = pd.read_csv("../python/info/Potions.csv", sep=",", low_memory=False)
        info3 = potions2.loc[Id-1, ["Id","name","img","effect","valuestype","val"]]
        id4 = info3["Id"]
        name4 = info3["name"]
        img4 = info3["img"]
        effect = info3["effect"]
        valuestype = info3["valuestype"]
        val = info3["val"]
        return [id4, name4, img4, effect, valuestype, val]
    

    def heal(self,potions):
        if self.joueur.hpmax == self.joueur.hp :
            return False 
        if self.joueur.hp + potions[5] <= self.joueur.hpmax :
            self.joueur.hp = self.joueur.hp + potions[5]
            return True 
        else : 
            self.joueur.hp = self.joueur.hpmax
            return True 
     
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
        
        
        # Image du joueur avec l'arme 
        
        jimg = self.joueur.moveimage["right"][0]
        jimg = pygame.transform.scale(jimg, (150*self.facteur, 150*self.facteur))
        jimg.set_colorkey((0, 0, 0))
        jimg_rect = jimg.get_rect()
        jimg_rect.x = 225*self.facteur
        jimg_rect.y = 175*self.facteur
        
        aimg = pygame.image.load(self.imga).convert_alpha()
        aimg = pygame.transform.scale(aimg,(75*self.facteur, 75*self.facteur))
        aimg = pygame.transform.flip(aimg, 180, 0)
        aimg.set_colorkey((0, 0, 0))
        aimg_rect = aimg.get_rect()
        aimg_rect.x = 295*self.facteur
        aimg_rect.y = 240*self.facteur
        
        # texte hp 
        
        pv = ClassPG.Texte("PV : "+str(self.joueur.hp), 575*self.facteur, 400*self.facteur, False)
        
        
        Hp_mob = ClassPG.progressbar(self.ennemii.Pv/self.ennemii.PvMax,  925*self.facteur, 130*self.facteur, 110*self.facteur,20*self.facteur)
        
        #Image de fond 
         
        Img = ClassPG.img("../img/temp/screen.png", 0, 0, self.size[0], self.size[1], False)
         
        # Compteur pour le tour par tour 
        
        compteur = 0 
        while running : 
            if not self.enfight: 
                running = False 
            
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    running = False
                if events.type == pygame.KEYDOWN : 
                    if events.key == pygame.K_ESCAPE :
                        self.gui = False 
                mousepos = pygame.mouse.get_pos()
                if events.type == pygame.MOUSEBUTTONDOWN and self.tour == True :
                    if events.button == 1: # 1= clique gauche
                        if self.gui == False :
                            # Bouton atk
                            if batk_rect.collidepoint(events.pos) :
                                self.ennemii.Pv -= self.realdmg
                                self.tour = False 
                                if self.ennemii.Pv <= 0 : 
                                    self.enfight = False
                            # Bouton fuir 
                            if bf_rect.collidepoint(events.pos):
                                self.enfight = False
                            if bobj_rect.collidepoint(events.pos):
                                self.afficherinv()
                                self.gui = True 
                if self.gui == True : 
                    for i in self.w :
                        if i.click(events, mousepos):
                            if i.obj.genre in ["potions"]:  
                                if self.dico[self.potions(i.obj.link)[3]](self.potions(i.obj.link)):
                                    pv.iupdate("PV : "+str(self.joueur.hp), (255, 255, 255), (pv.x, pv.y))
                                    self.tour = False 
                                    self.gui = False 
                                    self.joueur.inventaire.suppr_nb_obj(1, i.casenumber)
                            
                        
            # Tour du mob
            if self.tour == False:
                compteur +=1
                if compteur == 400 :
                    self.joueur.hp -= self.dmgmob
                    pv.iupdate("PV : "+str(self.joueur.hp), (255, 255, 255), (pv.x, pv.y))
                    if self.joueur.hp <= 0:
                        self.enfight = False
                elif compteur == 800:
                    compteur = 0
                    self.tour = True 
        

            Img.iblit(self.screen)
            Hp_mob.blit(self.screen, self.ennemii.Pv, self.ennemii.PvMax)
            self.screen.blit(self.ennemii.mobimg, self.ennemii.mobimg_rect)
            self.screen.blit(jimg, jimg_rect)
            self.screen.blit(aimg, aimg_rect)
            self.screen.blit(bottom, bottom_rect)
            pv.iblit(self.screen)
            
            if self.gui == False :
                self.screen.blit(bf, bf_rect)
                self.screen.blit(batk, batk_rect)
                self.screen.blit(bobj,bobj_rect)
            else : 
                for i in self.w:
                    i.iblit(self.screen)
                    
                    
            
            pygame.display.update()
         