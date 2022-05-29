import pygame
import ClassPG
import ennemi
import pandas as pd
import random as rd
from PIL import Image, ImageFilter
import valeurs
import numpy as np
import math

class fight():
    def __init__(self, joueur, mobid:int, lvlmob:int):
        self.enfight = True
        self.joueur = joueur
        self.mobid = mobid
        self.gui = False 
        self.dico = {"heal":self.heal, "degat":self.damage}
        self.w = []
        self.boss = [5,6,7,8]
        try:
            if self.joueur.get_item_in_inventory(5).obj.genre == "arme":
                self.armid = self.joueur.get_item_in_inventory(5).obj.link
            else:
                self.armid = 1
        except AttributeError:
            self.armid = 1
        self.lvlmob = lvlmob



        pygame.init()
        self.size = valeurs.valeur.screensize
        self.defaultsize = (1280, 720)
        self.facteur = self.size[0]/self.defaultsize[0]
        self.screen = pygame.display.set_mode(self.size, valeurs.valeur.toggle)
        self.read()
        # Pour savoir qui attaque en premier 
        if self.ennemii.Speed > self.joueur.speedfight:
            self.tour = False # False = tour du mob
        elif self.ennemii.Speed == self.joueur.speedfight:
            self.tour = rd.choice([False, True])
        else : 
            self.tour = True
        
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
            self.realdmg = 0
        self.dmgmob = self.ennemii.Atk//1.3 - self.joueur.deffence/4
        if self.dmgmob < 0:
            self.dmgmob = 0

    def animation(self, object, i):
        return object.x + 0.01 * (i)**2 + 5

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
    
    """---Potion fonction---"""

    # Potion de heal
    def heal(self,potions):
        if self.joueur.hpmax == self.joueur.hp :
            return False 
        if self.joueur.hp + potions[5] <= self.joueur.hpmax :
            self.joueur.hp = self.joueur.hp + potions[5]
            return True 
        else : 
            self.joueur.hp = self.joueur.hpmax
            return True 
        
    # Potion de dégat  
    def damage(self,potions):
        """
        Il prend une liste de potions et un personnage, et si la potion est une potion en pourcentage, il calcule les dégâts
        en fonction du pourcentage de la santé du personnage, puis soustrait ces dégâts de la santé du personnage.

        :param potions: [0] = nom, [1] = description, [2] = prix, [3] = quantité, [4] = type, [5] = valeur
        :return: Vrai
        """
        if potions[4] == "pourcent" :
            potions[5] = self.ennemii.Pv * (potions[5]/100)
        self.ennemii.Pv = self.ennemii.Pv - potions[5]
        return True 

    def endfight(self, gagnant):
        return gagnant

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
        lvltext = ClassPG.Texte(str(self.lvlmob), 980*self.facteur, 110*self.facteur, True)
        name = ClassPG.Texte(str(self.ennemii.Nom), 980*self.facteur, 50, True)

        Hp_mob = ClassPG.progressbar(self.ennemii.Pv/self.ennemii.PvMax,  925*self.facteur, 130*self.facteur, 110*self.facteur,20*self.facteur)
        
        #Image de fond
        Img = ClassPG.img("../img/temp/screen.png", 0, 0, self.size[0], self.size[1], False)
         
        # Compteur pour le tour par tour
        compteur = 0

        # Il crée une liste de valeurs x de jimg_rect.x à jimg_rect.x + 100, puis crée une liste de valeurs y à partir du
        # journal de ces valeurs x. Deplacement Joueur
        anim_x = np.arange(jimg_rect.x, jimg_rect.x + 100, 1)
        anim_arme_x = np.arange(aimg_rect.x, aimg_rect.x + 100, 1)
        player_move = False
        x = 0

        anim_mob_x = np.arange(self.ennemii.mobimg_rect.x, self.ennemii.mobimg_rect.x - 100, -1)
        ennemi_move = False
        x_m = 0


        while running : 
            if not self.enfight: 
                running = False
            
            # Vérification des événements dans le jeu.
            for events in pygame.event.get():
                if self.mobid not in self.boss:
                    if events.type == pygame.QUIT:
                        running = False
                if events.type == pygame.KEYDOWN : 
                    if events.key == pygame.K_ESCAPE:
                        self.gui = False 
                mousepos = pygame.mouse.get_pos()
                if events.type == pygame.MOUSEBUTTONDOWN and self.tour == True :
                    if events.button == 1: # 1= clique gauche
                        if self.gui == False :
                            # Bouton atk
                            if batk_rect.collidepoint(events.pos):
                                player_move = True
                                self.tour = False
                            # Bouton fuir 
                            if bf_rect.collidepoint(events.pos) and self.mobid not in self.boss:
                                return self.endfight("Fuite")

                            if bobj_rect.collidepoint(events.pos):
                                self.afficherinv()
                                self.gui = True

            # Vérifier si le joueur a cliqué sur une potion dans l'inventaire. Si c'est le cas, il vérifie si la potion
            # est utilisable. Si c'est le cas, il utilise la potion et met à jour la santé du joueur.
            if self.gui == True :
                for i in self.w :
                    if i.click(events, mousepos):
                        if i.obj.genre in ["potions"]:
                            if self.dico[self.potions(i.obj.link)[3]](self.potions(i.obj.link)):
                                pv.iupdate("PV : "+str(self.joueur.hp), (255, 255, 255), (pv.x, pv.y))
                                self.tour = False
                                self.gui = False
                                self.joueur.inventaire.suppr_nb_obj(1, i.casenumber)

            # Une animation simple d'un personnage en mouvement.
            if player_move:
                x += 1
                jimg_rect.x, jimg_rect.y = anim_x[x], 1/x + jimg_rect.y
                aimg_rect.x, aimg_rect.y = anim_arme_x[x], 1 / x + aimg_rect.y
                if x > len(anim_x) - 2:
                    player_move = False
                    self.ennemii.Pv -= self.realdmg
                    if self.ennemii.Pv <= 0:
                        Cloot = Loot(self.lvlmob, self.joueur)
                        Cloot.running()
                        return self.endfight("Player")

            elif not player_move:
                if x > 1:
                    x -= 1
                    jimg_rect.x, jimg_rect.y = anim_x[x], 1/x + jimg_rect.y
                    aimg_rect.x, aimg_rect.y = anim_arme_x[x], 1 / x + aimg_rect.y

            # Tour du mob
            if self.tour == False:
                compteur +=1
                if compteur == 400 :
                    ennemi_move = True
                elif compteur == 800:
                    compteur = 0
                    self.tour = True

            # Déplacer le sprite ennemi.
            if ennemi_move:
                x_m += 1
                self.ennemii.mobimg_rect.x, self.ennemii.mobimg_rect.y = anim_mob_x[x_m], 1 / x_m + self.ennemii.mobimg_rect.y
                if x_m > len(anim_mob_x) - 2:
                    ennemi_move = False
                    self.joueur.hp -= self.dmgmob
                    pv.iupdate("PV : " + str(self.joueur.hp), (255, 255, 255), (pv.x, pv.y))
                    if self.joueur.hp <= 0:
                        return self.endfight("Ennemis")
            elif not ennemi_move:
                if x_m > 1:
                    x_m -= 1
                    self.ennemii.mobimg_rect.x, self.ennemii.mobimg_rect.y = anim_mob_x[x_m], 1 / x_m + self.ennemii.mobimg_rect.y

            Img.iblit(self.screen)
            Hp_mob.blit(self.screen, self.ennemii.Pv, self.ennemii.PvMax)
            name.iblit(self.screen)
            lvltext.iblit(self.screen)
            self.screen.blit(self.ennemii.mobimg, self.ennemii.mobimg_rect)
            self.screen.blit(jimg, jimg_rect)
            self.screen.blit(aimg, aimg_rect)

            if self.gui == False :
                if self.tour == True:
                    self.screen.blit(bf, bf_rect)
                    self.screen.blit(batk, batk_rect)
                    self.screen.blit(bobj,bobj_rect)
            else : 
                for i in self.w:
                    i.iblit(self.screen)
            self.screen.blit(bottom, bottom_rect)
            pv.iblit(self.screen)

            pygame.display.update()
        return self.endfight("Fuite")

class Loot():
    def __init__(self, Id, joueur) : 
        self.joueur = joueur
        Argent = pd.read_csv("../python/info/Money.csv", sep=",", low_memory=False)
        info4 = Argent.loc[Id-1, ["Level","Argent"]]
        Lvl = info4["Level"]
        self.Money = info4["Argent"]
        
        
        self.screen = pygame.display.set_mode(valeurs.valeur.screensize, valeurs.valeur.toggle)
    
    def running(self):
        
        
        # Boutoun Recupérer
        Disp = False 
        recup = pygame.image.load("../img/Fight/Recup.png").convert_alpha()
        recup = pygame.transform.scale(recup, (200*valeurs.valeur.facteur,100*valeurs.valeur.facteur))
        recup_rect = recup.get_rect()
        recup_rect.x = 565 * valeurs.valeur.facteur
        recup_rect.y = 575 *  valeurs.valeur.facteur
        
        #Image de fond
        Img = ClassPG.img("../img/temp/screen.png", 0, 0, valeurs.valeur.screensize[0], valeurs.valeur.screensize[1], False)
        
        # Image de croix 
        Cross = pygame.image.load("../img/Fight/Recup.png").convert_alpha()
        Cross = pygame.transform.scale(Cross, (200*valeurs.valeur.facteur,100*valeurs.valeur.facteur))
        Cross_rect = Cross.get_rect()
        Cross_rect.x = 1260 * valeurs.valeur.facteur
        Cross_rect.y = 20 *  valeurs.valeur.facteur
        
        
        argent = ClassPG.Texte("Argent : "+str(self.joueur.money), 575* valeurs.valeur.facteur, 400* valeurs.valeur.facteur, False)
        argentwin = ClassPG.Texte("Argent gagnés :"+ str(self.Money),555* valeurs.valeur.facteur, 500* valeurs.valeur.facteur, False)
        running = True 
        while running :      
            # Vérification des événements dans le jeu.
            for events in pygame.event.get():

                if events.type == pygame.QUIT:
                    running = False
                if events.type == pygame.MOUSEBUTTONDOWN:
                    if events.button == 1: # 1= clique gauche
                        if recup_rect.collidepoint(events.pos) and Disp == False:
                            self.joueur.money += self.Money
                            Disp = True 
                            print(self.joueur.money)
                            running = False 
                        if Cross_rect.collidepoint(events.pos):
                            running = False 

            Img.iblit(self.screen)
            argent.iblit(self.screen)
            argentwin.iblit(self.screen)
            self.screen.blit(Cross,Cross_rect)
            if Disp == False :
                self.screen.blit(recup, recup_rect)
                  
            pygame.display.update()
            
        