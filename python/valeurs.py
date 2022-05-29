import pygame
import ClassPG as PG
import ast

class val():
    def __init__(self):
        self.screensize = (1280,720)
        self.volume = 0
        self.musique = PG.son('../Sons/poke-chill.mp3',"music")
        self.toggle = False
        self.l = {"up":pygame.K_z, "down" : pygame.K_s, "left":pygame.K_q, "right":pygame.K_d, "interact":pygame.K_e, "inventory":pygame.K_i}
        self.save_l = "first"
        self.name = "None" #PlayerName
        self.load()

    def load(self):
        set = open("Basesave/settings.txt", "r")
        L = set.readlines()
        self.toggle = ast.literal_eval(L[2].split(" ")[1])
        self.volume = float(L[0].strip().split(" ")[1])
        self.screensize = (int(L[1].split(" ")[1].split(",")[0]), int(L[1].split(" ")[1].split(",")[1]))

    def change_save_location(self, new):
        self.save_l = new

    def save(self):
        set = open("Basesave/settings.txt", "w")
        set.writelines("volume: "+str(self.volume )+"\n")
        set.writelines("resolution: "+str(self.screensize).replace(" ", "").replace ("(","").replace(")","")+"\n")
        set.writelines("FullScreen: "+str(self.toggle)+"\n")
        set.writelines("Name: " + str(self.name))
        set.close()

        set = open("Basesave/keybinding.txt", "w")
        for i in self.l.keys():
            print(i)
            set.writelines(str(i)+": "+str(self.l[i])+"\n")
        set.close()

    def screensize2(self,valeurs, display, fullscreen = False):
        if valeurs == None: valeurs = self.screensize
        if valeurs != self.screensize or fullscreen != self.toggle:
            self.screensize = valeurs
            self.toggle = fullscreen
            if fullscreen:
                display = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
            else :
                display = pygame.display.set_mode(self.screensize)

        self.facteur = self.screensize[0]/1280
        return display

valeur = val()