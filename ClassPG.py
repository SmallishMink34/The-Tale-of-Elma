import pygame
import sys


##=====================================================##
#	Fichier Python pour gerer les élements de pygame	#
##=====================================================##

class game:
    """Class qui gere la fenetre """

    def __init__(self, name, size, tick):
        # Lancement de pygame
        pygame.init()

        # Création de la fenetre de jeux
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(name)  # Choix du nom

        # Variable boolean Boucle de jeux
        self.running = True

        # Image de fond
        self.fond = pygame.image.load('image/background.png')
        self.fond = pygame.transform.scale(self.fond, size)

        # Vitesse du jeux
        self.clock = pygame.time.Clock()
        self.tick = tick

        # Touche
        self.pressed = {}

    def gameloop(self, screen):
        """Fonction de la boucle de jeu"""
        self.clock.tick(self.tick)  # Vitesse du jeux

        self.iblitall(screen)

    def eventpy(self):
        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                sys.exit()
            # gestion du clavier
            if event.type == pygame.KEYDOWN:  # si une touche a été tapée, le marque dans le dictionnaire pressed la
                # touche enfoncer
                self.pressed[event.key] = True
            if event.type == pygame.KEYUP:
                self.pressed[event.key] = False

    def iblitall(self, screen):
        """Fonction pour 'blit' les éléments sur l'écran"""

        # Fond
        screen.blit(self.fond, (0, 0))

        # Actualisation des éléments sur l'écran
        pygame.display.flip()


class Texte:
    """Class qui permet de créer des textes """

    def __init__(self, texte, x, y, center, color=(255, 255, 255), size=32, font='font/font.ttf'):
        self.texte = texte
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.font = pygame.font.Font(font, self.size)

        self.iupdate(self.texte)

        if center == 'center':  # Detecte si on veut que les coordonées sois centré ou non
            self.rect.centerx, self.rect.centery = x, y
        else:
            self.rect.x, self.rect.y = x, y

    def iupdate(self, texte, color=(255, 255, 255)):
        self.txt = self.font.render(str(texte), True, color)
        self.rect = self.texte.get_rect()

    def ihover(self, mousepos, color=(128, 255, 0)):
        """Detection du survol de la souris"""
        if self.rect.collidepoint(mousepos):
            self.texte = self.font.render(str(self.texte), True, color)
        else:
            self.texte = self.font.render(str(self.texte), True, self.color)

    def click(self, mousepos, event):
        """Detection du click de la souris et du survol"""
        self.ihover(mousepos)
        if self.rect.collidepoint(mousepos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

    def iblit(self, screen):
        """Affichage du texte"""
        screen.blit(self.texte, self.rect)


class bouton:
    """Class qui permet de crée des boutons facilement"""

    def __init__(self, image, x, y, w, h):
        self.link = image

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = pygame.image.load(self.link).convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

    def iblit(self, screen):
        """Affichage du bouton"""
        screen.blit(self.image, self.rect)

    def click(self, mousepos, event):
        """Detection du click de la souris et du survol"""
        self.ihover(mousepos)
        if self.rect.collidepoint(mousepos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

    def ihover(self, mousepos, imglink=None):
        """Detection du survol de la souris"""
        if self.rect.collidepoint(mousepos) and imglink is not None:
            self.image = pygame.image.load(imglink).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y

        else:
            self.image = pygame.image.load(self.link).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y


class son:
    """Class qui permet de crée une music ou un son"""

    def __init__(self, music, type):
        self.music = music  # Lien de la music
        self.type = type  # Type music ou song
        if self.type == 'song':
            self.song = pygame.mixer.Sound('song/' + self.music)
        elif self.type == 'music':
            self.song = pygame.mixer.music.load('song/' + self.music)

    def volume(self, number):
        """Modification du volume"""
        if self.type == 'song':
            self.song.set_volume(number)
        elif self.type == 'music':
            self.song = pygame.mixer.music.set_volume(number)

    def play(self):
        """Jouer la musique ou le song"""
        if self.type == 'song':
            self.song.play()
        elif self.type == "music":
            self.music = pygame.mixer.music.play(-1)

    def stop(self):
        """Stoper le song"""
        if self.type == 'music':
            self.music = pygame.mixer.music.stop()


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

        self.iupdate(self.link)

    def iupdate(self, image, upscale=True, upcoords=True):
        """Met a jour l'image"""
        self.image = pygame.image.load(image).convert_alpha()
        if upscale:
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
        if upcoords:
            self.rect = self.image.get_rect()
            if self.center:
                self.rect.centerx, self.rect.centery = self.x, self.y
            else:
                self.rect.x, self.rect.y = self.x, self.y

    def iblit(self, screen):
        """Affiche de l'image"""
        screen.blit(self.image, self.rect)


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
