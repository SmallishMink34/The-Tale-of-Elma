import game 
import ClassPG as PG

import pygame

class menu():
    def init(self) -> None:

        self.game = PG.game("Ingame", (self.display_w, self.display_h), 60)
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.image_fond= PG.img('img/Fond_Menu.png', 0, 0, 1920, 1080, True)
        self.b={}
        self.b['bouton_lancer']= PG.bouton()
        self.b['bouton_quitter'] = PG.bouton()
        self.b['bouton_para']= PG.bouton() 
        #Musique du menu 
        #self.musique = PG.son('sons/poke-chill.mp3',"music")
        #self.click = PG.son(,"song")
        self.d = {}
        self.d['text_Play'] = PG.Texte("Jouer",500,500,True,color=(255,255,255), size= 40, font='arial')
        self.d['text_Para']= PG.Texte("Paramètre")
        self.d['text_Quit'] = PG.Texte("Quitter",)

    def gameloop(self, event, screen):
        self.eventpy()
        self.iblit()

    def eventpy(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            x, y = pygame.mouse.get_pos()

    def iblit(self, screen):
        for i in self.d.keys():
            self.d[i].iblit()
        for n in self.b.keys():
            self.b[n].iblit()


    def run(self):
        continuer = True

        while continuer:
            self.game.screen.blit(self.display, (0, 0))
            self.gameloop(pygame.event.get(), self.display)
            pygame.display.update()
        pygame.quit()


menu = menu()
menu.run()