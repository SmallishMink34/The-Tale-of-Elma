import game 
import ClassPG as PG

import pygame

class menu():
    def __init__(self) -> None:
        self.display_w,self.display_h = 1280,720
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60)
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.image_fond= PG.img('../img/Fond_Menu.png', 0, 0, 1280, 720, False)
        #Musique du menu 
        self.musique = PG.son('../Sons/poke-chill.mp3',"music")
        self.musique.play()
        self.musique.volume(0.02)
        self.d = {}
        self.d['text_Play'] = PG.Texte("Jouer",560,320,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['text_Para']= PG.Texte("Parametres",520,440,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')
        self.d['text_Quit'] = PG.Texte("Quitter",545,570,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')

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
                gamee.run()
            if self.d['text_Quit'].click((x,y), event, color=(128, 255, 0)):
                pygame.quit()
            if self.d['text_Para'].click((x,y), event, color=(128, 255, 0)):
                self.continuer = False
                paraa = para()
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
    def __init__(self) -> None:
        self.display_w,self.display_h = 1280,720
        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60)
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.image_fond= PG.img('../img/Fond_Menu.png', 0, 0, 1280, 720, False)
        self.d = {}
        self.d['text_Quit'] = PG.Texte("Quitter",545,570,True,color=(255,255,255), size= 50, font='../font/Like Snow.otf')

    def gameloop(self, event, screen):
        self.eventpy(event)
        self.iblit(screen)
        

    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.continuer = False
            x, y = pygame.mouse.get_pos()
            if self.d['text_Quit'].click((x,y), event, color=(128, 255, 0)):
                pygame.quit()
                
                
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
    


menu = menu()
menu.run()