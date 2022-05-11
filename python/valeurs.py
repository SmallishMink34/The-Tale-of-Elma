import pygame
import ClassPG as PG

class val():
    def __init__(self):
        self.screensize = (1280,720)
        self.volume = 0
        self.musique = PG.son('../Sons/poke-chill.mp3',"music")
        self.toggle = False
        self.l = {"up":pygame.K_z, "down" : pygame.K_s, "left":pygame.K_q, "right":pygame.K_d, "interact":pygame.K_e, "inventory":pygame.K_i}

    def save(self):
        set = open("../python/save/settings.txt","w")
        set.writelines("volume: "+str(self.volume )+"\n")
        set.writelines("resolution: "+str(self.screensize).replace(" ", "").replace ("(","").replace(")","")+"\n")
        set.writelines("FullScreen: "+str(self.toggle))
        set.close()

        set = open("../python/save/keybinding.txt", "w")
        for i in self.l.keys():
            print(i)
            set.writelines(str(i)+": "+str(self.l[i])+"\n")
        set.close()

    def screensize2(self,valeurs, display, fullscreen = False):
        if valeurs != self.screensize or fullscreen != self.toggle:
            self.screensize = valeurs
            self.toggle = fullscreen
            if fullscreen:
                display = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
            else :
                display = pygame.display.set_mode(self.screensize)
        return display

valeur = val()