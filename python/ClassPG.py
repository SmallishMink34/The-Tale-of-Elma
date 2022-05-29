import math

import pygame
import sys

from pygame.constants import FULLSCREEN


##=====================================================##
#	Fichier Python pour gerer les élements de pygame	#
##=====================================================##

class game:
    """Class qui gere la fenetre """

    def __init__(self, name, size, tick, fullscreen=None):
        # Lancement de pygame
        pygame.init()



        # Création de la fenetre de jeux
        if fullscreen is False:
            self.screen = pygame.display.set_mode(size)
        else:
            self.screen = pygame.display.set_mode((size), FULLSCREEN)
        pygame.display.set_caption(name)  # Choix du nom
        pygame.display.set_icon(pygame.image.load("../img/icone.png").convert_alpha())
        self.w, self.h = self.screen.get_size()

        # Variable boolean Boucle de jeux
        self.running = True

        # Image de fond
        self.fond = img('../img/menu/background.jpg', 0, 0, size[0], size[1])

        # Vitesse du jeux
        self.clock = pygame.time.Clock()
        self.tick = tick

        # Element du jeux a blit
        self.telement = []
        self.ielement = []

        # Touche
        self.pressed = {}

    def gameloop(self):
        """Fonction de la boucle de jeu"""
        self.clock.tick(self.tick)  # Vitesse du jeux

    def eventpy(self):
        """
        La fonction parcourt tous les événements qui se sont produits depuis le dernier appel de la fonction.

        Si l'événement est un clic de souris, la fonction vérifie si le clic de souris s'est produit sur l'un des boutons.

        Si le clic de la souris était sur un bouton, la fonction imprime le texte du bouton
        """
        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                sys.exit()
            # gestion du clavier
            if event.type == pygame.KEYDOWN:  # si une touche a été tapée, le marque dans le dictionnaire pressed la
                # touche enfoncer
                self.pressed[event.key] = True
            if event.type == pygame.KEYUP:
                self.pressed[event.key] = False
            for i in self.telement:
                if i.click((x, y), event):
                    print('button click ' + str(i.texte))

    def iblitall(self):
        """Fonction pour 'blit' les éléments sur l'écran"""

        # Fond
        self.fond.iblit(self.screen)

        for i in self.ielement:
            i.iblit(self.screen)

        for i in self.telement:
            i.iblit(self.screen)

        # Actualisation des éléments sur l'écran
        pygame.display.flip()


class Texte:
    """Class qui permet de créer des textes """

    def __init__(self, texte, x, y, center, color=(255, 255, 255), size=32, font=''):
        self.texte = texte
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        try:
            self.font = pygame.font.Font(font, self.size)
        except FileNotFoundError:
            self.font = pygame.font.SysFont("Arial", self.size)
        self.center = center

        self.iupdate(self.texte, self.color)
        if center == 'center' or center == True:  # Detecte si on veut que les coordonées sois centré ou non
            self.rect.centerx, self.rect.centery = x, y
        else:
            self.rect.x, self.rect.y = x, y

    def iupdate(self, texte, color, coord=(0, 0)):
        self.txt = self.font.render(str(texte), True, color)
        self.rect = self.txt.get_rect()

        if self.center == 'center' or self.center == True:  # Detecte si on veut que les coordonées sois centré ou non
            self.rect.centerx, self.rect.centery = coord[0], coord[1]
        else:
            self.rect.x, self.rect.y = coord[0], coord[1]

    def updatecoords(self, x, y):
        self.rect.x, self.rect.y = x, y

    def ihover(self, mousepos, color=(128, 255, 0)):
        """Detection du survol de la souris"""
        if self.rect.collidepoint(mousepos):
            self.texte = self.font.render(str(self.texte), True, color)
        else:
            self.texte = self.font.render(str(self.texte), True, self.color)

    def click(self, mousepos, event, color=(128, 255, 0)):
        """Detection du click de la souris et du survol"""
        self.ihover(mousepos, color)
        if self.rect.collidepoint(mousepos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

    def iblit(self, screen):
        """Affichage du texte"""
        screen.blit(self.txt, self.rect)


class bouton(pygame.sprite.Sprite):
    """Class qui permet de crée des boutons facilement"""

    def __init__(self, image, x, y, w, h, center=False, toggle=False, toggletrue=None):
        self.link = image
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.toggle = toggle
        self.toggle_verif = toggletrue
        self.image = pygame.image.load(self.link).convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))

        self.img_copy = self.image.copy()

        self.shakesprite = {'-1': pygame.transform.rotate(self.image, 2), '0': self.image ,'1': pygame.transform.rotate(self.image, -2)}

        self.rect = self.image.get_rect()
        self.center = center

        if self.center:
            self.rect.centerx = x
            self.rect.centery = y
        else:
            self.rect.x, self.rect.y = x, y

    def iblit(self, screen):
        """Affichage du bouton"""
        screen.blit(self.image, self.rect)

    def click(self, mousepos, event, hover=False):
        """Detection du click de la souris et du survol"""
        if hover:
            self.ihover(mousepos)

        if self.rect.collidepoint(mousepos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.toggle:
                    if self.toggle_verif:
                        self.image = pygame.image.load(self.link[:-4] + "_off.png").convert_alpha()
                        self.image = pygame.transform.scale(self.image, (self.w, self.h))
                        self.rect = self.image.get_rect()
                        if self.center:
                            self.rect.centerx = self.x
                            self.rect.centery = self.y
                        else:
                            self.rect.x, self.rect.y = self.x, self.y
                        self.toggle_verif = False
                    else:
                        self.toggle_verif = True
                        self.image = pygame.image.load(self.link).convert_alpha()
                        self.image = pygame.transform.scale(self.image, (self.w, self.h))
                        self.rect = self.image.get_rect()
                        if self.center:
                            self.rect.centerx = self.x
                            self.rect.centery = self.y
                        else:
                            self.rect.x, self.rect.y = self.x, self.y
                return True

    def shake(self, x):
        self.image = self.shakesprite[str(int(math.cos(x)*2))]

    def ihover(self, mousepos, imglink=None):
        """Detection du survol de la souris"""
        if self.rect.collidepoint(mousepos) and imglink is not None:
            self.image = pygame.image.load(imglink).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            if self.center:
                self.rect.centerx = self.x
                self.rect.centery = self.y
            else:
                self.rect.x, self.rect.y = self.x, self.y

        else:
            self.image = pygame.image.load(self.link).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            if self.center:
                self.rect.centerx = self.x
                self.rect.centery = self.y
            else:
                self.rect.x, self.rect.y = self.x, self.y


class son:
    """Class qui permet de crée une music ou un son"""

    def __init__(self, music, type):
        """

        :param music: str [link]
        :param type: str [song | music]
        """
        self.music = music  # Lien de la music
        self.type = type  # Type music ou song
        self.playing = False
        pygame.mixer.init()
        if self.type == 'song':
            self.song = pygame.mixer.Sound(self.music)
        elif self.type == 'music':
            self.song = pygame.mixer.music.load(self.music)

    def volume(self, number):
        """Modification du volume"""
        if self.type == 'song':
            self.song.set_volume(number)
        elif self.type == 'music':
            self.song = pygame.mixer.music.set_volume(number)

    def play(self):
        """Jouer la musique ou le song"""
        self.playing = True
        if self.playing == True:
            if self.type == 'song':
                self.song.play()
            elif self.type == "music":
                self.music = pygame.mixer.music.play(-1)

    def stop(self):
        """Stoper le song"""
        if self.type == 'music':
            self.music = pygame.mixer.music.stop()
            self.playing = False


class rectangle():
    """Class Créant des rectangles """


class progressbar:
    """Class qui permet de crée une barre de progression, Utilise pour afficher la vie d'un boss"""

    def __init__(self, pourcent, x, y, w, h, color=(255, 0, 0)):
        self.pourcent = pourcent  # Pourcentage actuel
        self.x, self.y, self.w, self.h = x, y, w, h
        self.color = color

    def blit(self, screen, value, valuebase):
        """Affichage de la progress bar"""
        self.pourcent = value / valuebase  # Calcule du pourcentage (valeur de 0 a 1)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(self.x + 5, self.y + 5, (self.w - 10) * self.pourcent, self.h - 10))


class img(pygame.sprite.Sprite):
    """Class qui crée une image, peut etre animer grace a la class animate_img"""

    def __init__(self, image, x, y, w, h, center=True):
        super().__init__()
        self.link = image  # Image
        self.x = x  # Coordonées en x
        self.y = y  # Coordonées en y
        self.w = w  # Largeur de l'image
        self.h = h  # Hauteur de l'image
        self.center = center
        self.name = "aaa"  # Nothing
        self.type = "Collision"  # Nothing

        self.iupdate(self.link)

    def iupdate(self, image, upscale=True, upcoords=True):
        """Met a jour l'image"""
        self.image = pygame.image.load(image).convert_alpha()
        if upscale:
            self.image = pygame.transform.scale(self.image, (int(self.w), int(self.h)))
        if upcoords:
            self.rect = self.image.get_rect()
            if self.center:
                self.rect.centerx, self.rect.centery = self.x, self.y
            else:
                self.rect.x, self.rect.y = self.x, self.y

    def iblit(self, screen, flags=False):
        """Affiche de l'image"""
        screen.blit(self.image, self.rect)

    def get_recte(self):
        return self.rect


class animate_img(pygame.sprite.Sprite):
    """Class pour animer une image"""

    def __init__(self, imagebase, number, vitesse=1):
        super().__init__()
        self.imagebase = imagebase  # Image de base
        self.number = number  # Nombre d'image
        self.vitesse = vitesse  # Vitesse de l'animation (diviseur de 1)
        self.counter = 0  # Image actuel
        self.sprites = []  # Liste contenant toute les images

        # Generations des images
        for i in range(number):
            if self.imagebase[-6: -4] != '_0':  # Si le caratère '_0' n'existe pas dans le lien de l'image
                print(self.imagebase)
                self.sprites.append(pygame.image.load(self.imagebase[:-4] + f'_{str(i)}' + self.imagebase[-4:]))
            else:
                self.imagebase = self.imagebase.replace('_0', '_' + str(i))
                self.sprites.append(pygame.image.load(self.imagebase))

    def animation(self, image):
        """Animation de l'image a mettre dans une boucle"""
        self.counter += self.vitesse
        image.iupdate(self.sprites[self.counter], True)


class TextEntry:
    def __init__(self, win, couleur, rect, type, center=False, sizetxt=30):
        self.text = ""
        self.couleur = couleur
        self.font = pygame.font.SysFont("Arial", sizetxt)
        self.blit_text = None
        self.center = center
        self.rect = pygame.Rect(rect)
        if self.center:
            self.rect.centerx, self.rect.centery = rect[0], rect[1]

        self.sizetxt = sizetxt

        self.h = rect[3]
        self.w = rect[2]

        self.text_autorise = """ azertyuiopqsdfghjklmwxcvbn&éABCDEFGHIJKLMOPQRSTUVWXYZ"'(-è_çà)=^$*ù!:;,?./§%µ1478963250&éç"""
        self.select = False
        self.type = type

    def get_text(self):
        '''Return le texte'''
        return self.text

    def set_selection(self, events):
        '''Permet de selectioner l'entry'''
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.select = True
                else:
                    self.select = False

    def generer_affichage(self):
        """Permet de generer l'affichage """
        if self.type == "text":
            self.blit_text = self.font.render(self.text, True, (0, 0, 0))
        if self.type == "password":
            self.blit_text = self.font.render(str(len(self.text) * "*"), True, (0, 0, 0))
        self.recttxt = self.blit_text.get_rect()
        self.recttxt.x, self.recttxt.centery = self.rect[0], self.rect[1] + self.font.size("j")[1] / 2

    def get_keyboard_input(self, events):
        """Permet de recuperer les inputs"""
        pygame.key.set_repeat(300, 20)

        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.unicode in self.text_autorise and self.font.size(self.text + "M")[0] < self.w:
                    self.text += event.unicode
                    if len(self.text) > 25:
                        self.font = pygame.font.Font("../font/Like Snow.otf", self.sizetxt // 3 * 2)
                    else:
                        self.font = pygame.font.Font("../font/Like Snow.otf", self.sizetxt)
                    self.generer_affichage()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.generer_affichage()

    def iblit(self, events, screen):
        """Permet l'affichage finale"""
        self.set_selection(events)
        if self.select:
            self.get_keyboard_input(events)

        pygame.draw.rect(screen, self.couleur, self.rect)
        if self.text:
            screen.blit(self.blit_text, self.recttxt)

        if self.select:
            if self.text:
                text_rect = self.blit_text.get_rect()
                pygame.draw.rect(screen, (0, 140, 200), [self.rect[0] + text_rect[2], self.rect[1], 1, self.rect[3]])
            else:
                pygame.draw.rect(screen, (0, 150, 200), [self.rect[0], self.rect[1], 1, self.rect[3]])
