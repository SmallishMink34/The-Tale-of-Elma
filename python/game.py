import pygame
import ClassPG
import ClassPlayer
import map
import Gui
import inv

class Game():
    """
    Class du jeux
    """
    def __init__(self):
        self.display_w, self.display_h = 1280, 720

        self.game = ClassPG.game("Ingame", (self.display_w, self.display_h), 60)

        self.display = pygame.Surface((self.display_w, self.display_h))

        self.player = ClassPlayer.PlayerTopDown("SmallIshMink",(0, 0), self.display)

        self.map_manag = map.Mapmanager( self.display, self.player)



    def run(self):
        """
        Mise en marche du jeux
        :return: Nothing
        """
        inv_ = False
        inv_clique = True
        running = True
        clock = pygame.time.Clock()

        LEFT = 1
        RIGHT = 3
        inventaire = inv.inv("Inventaire","../img/img.inv/personnage_test.png")
        move = False


        while running:

            self.game.screen.blit(self.display, (0, 0))

            self.map_manag.updating() # Met a jour la carte et le joueur
            self.map_manag.draw() # Dessine la carte


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    self.player.pressed[event.key] = True
                if event.type == pygame.KEYUP:
                    self.player.pressed[event.key] = False

                if inv_:
                    if not move:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                                case0 = inventaire.quelle_case(event)
                                move = inventaire.click(event,case0)
                    else:
                        if inventaire.quelle_case(event)!= False:
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                                case = inventaire.quelle_case(event)
                                inventaire.move(case0,case)
                                move = False
                if move:
                    inventaire.image_suivie(case0,(x,y))

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    objet = inv.objet("casque",1,"armure","../img/item/diamond_helmet.png","c1")
                    objet2 = inv.objet("plastron",1,"armure","../img/item/diamond_chestplate.png","c2")
                    inventaire.add(objet.recup())
                    inventaire.add(objet2.recup())

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        if inv_clique:
                            inv_ = True
                            inv_clique = False

                        else:
                            inv_ = False
                            inv_clique = True
            if inv_:
                inventaire.iblit(self.display)
            clock.tick(60)
            pygame.display.update()
        pygame.quit()



game = Game()
game.run()
