import pygame
import ClassPG
import ClassPlayer
import map
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

        self.map_manag = map.Mapmanager(self.display, self.player)


    def run(self):
        """
        Mise en marche du jeux
        :return: Nothing
        """
        running = True
        clock = pygame.time.Clock()

        inventaire = inv.inv("Inventaire","../img/img.inv/personnage_test.png")


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
                self.player.gui.event((x, y), event)

                if self.player.pressed.get(pygame.K_i):
                    self.player.gui.inventory(inventaire)
                    self.player.pressed[pygame.K_i] = False


            self.player.gui.iblit(self.display)
            clock.tick(60)
            pygame.display.update()
        pygame.quit()



game = Game()
game.run()
