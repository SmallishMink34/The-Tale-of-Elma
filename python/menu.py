import game 
import ClassPG as PG
import pygame
import pygame_widgets as pw 
from pygame_widgets.slider import Slider


class menu():
    def __init__(self) -> None:
        self.display_w,self.display_h = 1280,720
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60)
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.image_fond= PG.img('../img/menu/Fond_Menu.png', 0, 0, 1280, 720, False)
        #Musique du menu 
        self.musique = PG.son('../Sons/poke-chill.mp3',"music")
        self.musique.play()
        self.musique.volume(0.3)
        self.d = {}
        self.d['text_Play'] = PG.Texte("Jouer",560,320,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['text_Para']= PG.Texte("Parametres",520,440,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['text_Quit'] = PG.Texte("Quitter",545,570,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['Titre'] = PG.Texte("Titre",500,50,True,color=(255,255,255), size= 100, font='../font/Like Snow.otf')

    def gameloop(self, event, screen):
        self.eventpy(event)
        self.iblit(screen)


    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['text_Play'].click((x,y), event, color=(128, 255, 0)):
                self.continuer = False
                gamee = game.Game()
                self.musique.stop()
                gamee.run()
            if self.d['text_Quit'].click((x,y), event, color=(128, 255, 0)):
                pygame.quit()
            if self.d['text_Para'].click((x,y), event, color=(128, 255, 0)):
                self.continuer = False
                paraa = para(self)
                paraa.run()
                   
    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)


    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.display, (0, 0))
            self.gameloop(pygame.event.get(), self.display)
            pygame.display.update()
        pygame.quit()


class para():
    def __init__(self,menu) -> None:
        self.display_w,self.display_h = 1280,720
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60)
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.image_fond= PG.img('../img/menu/Fond_Menu.png', 0, 0, 1280, 720, False)
        self.d = {}
        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png',1230,670,50,50)
        self.d['Musique']= PG.Texte("Musique",535,440,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['Touche'] = PG.Texte("Touches",530,560,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['Skin'] = PG.Texte("Cosmetiques",500,320,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.menu = menu

    def gameloop(self, event, screen):
        self.eventpy(event)
        self.iblit(screen)
        

    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x,y), event) :
                self.continuer = False
                menuu = menu()
                menuu.run()
            if self.d['Musique'].click((x,y), event):
                musi = song(self.menu)
                musi.run()
                
                
    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)


    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.display, (0, 0))
            self.gameloop(pygame.event.get(), self.display)
            pygame.display.update()
        pygame.quit()
    
class song():
    def __init__(self,menu) -> None:
        self.display_w,self.display_h = 1280,720
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60)
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.image_fond= PG.img('../img/menu/Fond_Menu.png', 0, 0, 1280, 720, False)
        self.d = {}
        self.d['Quitter'] = PG.bouton('../img/menu/Quit.png',1230,670,50,50)
        self.slider = Slider(self.display, 250, 330, 800, 40, min=0, max=99, step = 1, initial=20, curved=True, handleRadius=30)
        self.d['Volume'] = PG.Texte('Volume : 0', 120, 120, True)
        self.menu = menu
    def gameloop(self, event, screen):
        
        self.iblit(screen)
        self.eventpy(event)

    def eventpy(self, events):
        for event in events:
            self.d['Volume'].iupdate("Volume : "+str(self.slider.getValue())+"%", (255, 255, 255), (600, 400))
            self.menu.musique.volume(self.slider.getValue()/100)
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['Quitter'].click((x,y), event) :
                self.continuer = False
                menuu = menu()
                menuu.run()

        pw.update(events)

    def iblit(self, screen):
        self.image_fond.iblit(screen)
        for i in self.d.keys():
            self.d[i].iblit(screen)
        


    
    def run(self):
        self.continuer = True
        while self.continuer:
            self.game.screen.blit(self.display, (0, 0))
            self.gameloop(pygame.event.get(), self.display)
            pygame.display.update()
        pygame.quit()

        



menue = menu()
menue.run()