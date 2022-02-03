import pygame
import ClassPG
import ClassPlayer
from pygame.locals import *
import sys
import pyscroll
import pytmx
import inv
import time

class Game():
    """
    Class du jeux
    """
    def __init__(self):
        self.display_w, self.display_h = 1280, 720

        self.game = ClassPG.game("Ingame", (self.display_w, self.display_h), 60)

        self.tmx = pytmx.util_pygame.load_pygame("img/tile/Lobby.tmx")
        mapdata = pyscroll.data.TiledMapData(self.tmx)
        map_layer = pyscroll.orthographic.BufferedRenderer(mapdata, (self.display_w, self.display_h))
        map_layer.zoom = 1.6

        player_pos = self.tmx.get_object_by_name("PlayerPos") # Endroit de spawn du joueur (défini sur Tiled)
        self.player = ClassPlayer.PlayerTopDown((player_pos.x, player_pos.y))

        self.mapsize_x = self.tmx.width #Taille x de la map
        self.mapsize_y = self.tmx.height #Taille y de la map
        self.tile_size = self.tmx.tilewidth #Taille de chaque tile

        self.range = 5

        self.walls = []
        self.objects_input = []

        for obj in self.tmx.objects: #Ajout des collsion dans des listes
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "Input_Collision":
                self.objects_input.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.map = []
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7) #groupe contenant le joueur et la map
        self.group.add(self.player)

    def run(self):
        """
        Mise en marche du jeux
        :return: Nothing
        """
        inv_ = False
        inv_clique = True
        running = True
        clock = pygame.time.Clock()
        display = pygame.Surface((self.display_w, self.display_h))
        LEFT = 1
        RIGHT = 3
        inventaire = inv.inv("Inventaire","img/img.inv/personnage_test.png")
        move = False
        while running:
            self.game.screen.fill((255, 25, 48))
            self.game.screen.blit(display, (0, 0))

            self.player.location_old() #Savegarde des position du joueur avant mouvement

            self.group.update() # Met a jour la carte et le joueur
            self.group.center(self.player.rect.center) #Centre la carte sur le joueur

            self.group.draw(display) #Dessin de la carte et du joueur


            self.player.dirrection() #Deplacement joueur

            
                    
            for i in self.group.sprites():
                if i.feet.collidelist(self.walls) > -1: #si les pieds du joueurs entre en collision avec un objet
                    i.moveback()
                if i.rect.collidelist(self.objects_input) > -1:#si le joueurs entre en collision avec un objet
                    i.inputaction()
            

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
                    objet = inv.objet("casque",64,"armure","img/item/diamond_helmet.png","c1")
                    objet2 = inv.objet("plastron",64,"armure","img/item/diamond_chestplate.png","c2")
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
                inventaire.iblit(display)
            clock.tick(60)
            pygame.display.update()
        pygame.quit()



game = Game()
game.run()
