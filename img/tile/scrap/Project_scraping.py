import pygame
import sys # pour fermer correctement l'application
import bs4 as bs
import urllib.request
pygame.init()

class TextEntry:
    def __init__(self, win, couleur, rect, type, sizetxt=30):
        self.win = win
        self.text = ""
        self.couleur = couleur
        self.font = pygame.font.SysFont("Arial", sizetxt)
        self.blit_text = None
        self.rect = pygame.Rect(rect)
        self.sizetxt = sizetxt
        self.h = rect[3]
        self.w = rect[2]

        print(self.h)

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
        self.recttxt.x, self.recttxt.centery = self.rect[0], self.rect[1] + self.font.size("j")[1]

    def get_keyboard_input(self, events):
        """Permet de recuperer les inputs"""
        pygame.key.set_repeat(300, 20)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.unicode in self.text_autorise:
                    self.text += event.unicode
                    if len(self.text) > 25:
                        self.font = pygame.font.SysFont("Arial", self.sizetxt // 3 * 2)
                    else:
                        self.font = pygame.font.SysFont("Arial", self.sizetxt)
                    self.generer_affichage()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.generer_affichage()

    def afficher(self, events):
        """Permet l'affichage finale"""
        self.set_selection(events)
        if self.select:
            self.get_keyboard_input(events)

        pygame.draw.rect(self.win, self.couleur, self.rect)
        if self.text:
            self.win.blit(self.blit_text, self.recttxt)

        if self.select:
            if self.text:
                text_rect = self.blit_text.get_rect()
                pygame.draw.rect(self.win, (0, 140, 200), [self.rect[0] + text_rect[2], self.rect[1], 1, self.rect[3]])
            else:
                pygame.draw.rect(self.win, (0, 150, 200), [self.rect[0], self.rect[1], 1, self.rect[3]])


class rectangle():
    """Class Créant des rectangles """
    def __init__(self, x, y, w, h, color=(255, 255, 255), cornerradius=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.cornerradius = cornerradius
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def iblit(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0, self.cornerradius)

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y



def boyermoore():
    # Création de la musique
    pygame.mixer.music.load("musique.mp3")
    son = pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    #Création de la fenetre de base
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Scrap")

    # Fond
    fond = pygame.image.load("Back.jpg")
    fond = pygame.transform.scale(fond, (800, 600))

    # Bouton quitter
    Q = pygame.image.load("Quitter.png").convert_alpha()
    Q = pygame.transform.scale(Q, (50, 50))
    Q_rect = Q.get_rect()
    Q_rect.x = 740
    Q_rect.y = 540

    #Bouton lancement de la recherche
    r = pygame.image.load("Rechercher.png").convert_alpha()
    r = pygame.transform.scale(r, (75, 75))
    r_rect = r.get_rect()
    r_rect.x=350
    r_rect.y=225

    # Texte 1
    police = pygame.font.Font("police.ttf", 20)
    texte = police.render("Le thème de votre chanson est  : ", True, pygame.Color("#000000"))
    texte_rect = texte.get_rect()
    texte_rect.x = 220
    texte_rect.y = 425

    # Texte 2
    police = pygame.font.Font("police.ttf", 40)
    texte2 = police.render("Boyer-moore ", True, pygame.Color("#000000"))
    texte2_rect = texte.get_rect()
    texte2_rect.x, texte2_rect.y = 240, 75


    # Affichage du theme

    file = open('chanson.txt', "r")
    paroles = file.read()
    file.close()

    # Boyer-moore

    def table_sauts(cle):
        # crée un dico qui à chaque lettre renvoie son décalage
        d = {}
        for i in range(len(cle) - 1):
            d[cle[i]] = len(cle) - i - 1
        return d

    def boyer_moore(texte, cle):
        long_txt = len(texte)
        long_cle = len(cle)
        positions = []  # liste des positions où l'on trouve le motif
        if long_cle <= long_txt:
            decalage = table_sauts(cle)  # on charge la table des décalages
        i = 0
        trouve = False
        while (i <= long_txt - long_cle):
            for j in range(long_cle - 1, -1,-1):  # On part du dernier indice de la cle jusque 0 en décalant de -1 à chaque fois
                trouve = True
                if texte[i + j] != cle[j]:  # Si on tombe sur une lettre différentes de celle de la clé
                    if texte[i + j] in decalage and decalage[texte[i + j]] <= j:
                        i += decalage[texte[i + j]]  # on décale dans le texte en utilisant la table de décalage
                    else:
                        i += j + 1  # si la lettre n'est pas dans la table de décalage alors on décale du nombre de lettres restantes à explorer sur la clé
                    trouve = False
                    break  # on sort de la boucle for car on a trouvé une lettre qui ne convient pas
            if trouve:  # si toutes les lettres convenait donc on a trouvé une occurence de la clé dans texte
                positions.append(i)  # on ajoute à la liste des positions où l'on trouve la clé dans le texte
                i = i + 1
                trouve = False  # on remet trouvé à False car on cherche la prochaine occurence
        return positions

    def maxi(tab):
        u = tab[0]
        for i in range(len(tab)):
            if tab[i] >= u:
                u = tab[i]
        return u

    def get_info(texte):
        theme = {'Amour': [0, ['accouplement', 'admiration', 'adoration', 'adultère', 'affect', 'affection',
                               'altruisme', 'amativité', 'amitié', 'amourette', 'amusement', 'ange', 'Aphrodite',
                               'archer', 'archerot', 'ardeur', 'éros', 'association', 'attachement', 'attraction',
                               'aventure', 'babiole', 'badinage', 'bagatelle', 'béguin', 'baise', 'batifolage',
                               'biquet', 'biquette', 'bluette', 'bouillonnement', 'bricole', 'caprice', 'chaleur',
                               'charité', 'coït', 'coeur', 'concubinage', 'concupiscence', 'conquête',
                               'copulation', 'coquetterie', 'culte', 'cupidon', 'Cupidon', 'débauche',
                               'délicatesse', 'désir', 'dévotion', 'dévouement', 'dilection', 'enfant',
                               'engouement', 'entente', 'enthousiasme', 'estime', 'faible', 'fanatisme',
                               'fantaisie', 'ferveur', 'feu', 'fièvre', 'flamme', 'fleurette', 'flirt', 'folie',
                               'fréquentation', 'fraternité', 'galanterie', 'goût', 'grâce', 'hyménée', 'hymen',
                               'idolâtrie', 'inceste', 'inclination', 'intérêt', 'intrigue', 'ivresse',
                               'lascivité', 'liaison', 'libertinage', 'luxure', 'maladie', 'mariage',
                               'marivaudage', 'mouvement', 'mysticisme', 'passade', 'passion', 'passionnette',
                               'penchant', 'philanthropie', 'piété', 'plaisir', 'pulsion', 'relation', 'rut',
                               'sens', 'sensibilité', 'sentiment', 'tendance', 'tendresse', 'toquade', 'touche',
                               'union', 'vénération', 'Vénus']],
                 'Mort': [0, ['écroulement', 'agonie',
                              'anéantissement', 'ankylosé',
                              'apathique', 'épuisé', 'éreinté',
                              'assassinat', 'éteint', 'évanoui',
                              'brisé', 'cadavre', 'camarde',
                              'chute', 'claqué', 'condamné',
                              'corps', 'crève', 'crevé',
                              'croupissant', 'décédé', 'décès',
                              'décomposition', 'défunt', 'délavé',
                              'dépouille', 'désert', 'détruit',
                              'decujus', 'dernierjour',
                              'derniersommeil', 'derniersoupir',
                              'destruction', 'deuil',
                              'disparition', 'disparu', 'dormant',
                              'effondrement', 'enterrement',
                              'enveloppe', 'esprit', 'esquinté',
                              'euthanasie', 'exécution', 'excédé',
                              'exténué', 'extinction', 'fade',
                              'fantôme', 'faucheuse', 'feu',
                              'fichu', 'figé', 'fin', 'fini',
                              'flapi', 'fossoyeuse', 'foutu',
                              'grandvoyage', 'harassé', 'immobile',
                              'inanimé', 'inerte', 'inhabité',
                              'insensible', 'irrécupérable',
                              'ivre', 'languide', 'laParque',
                              'lessivé', 'macchab', 'macchabée',
                              'malemort', 'mânes', 'meurtre',
                              'morne', 'mortifié', 'morts',
                              'mourant', 'néant', 'nécrosé',
                              'nuitéternelle', 'ombre', 'parque',
                              'passé', 'perdu', 'perte', 'plat',
                              'plongeon', 'rétamé', 'recru',
                              'rendu', 'repos', 'reposéternel',
                              'restes', 'rompu', 'ruine',
                              'silencieux', 'sommeiléternel',
                              'somnolent', 'spectre', 'stagnant',
                              'supplice', 'terne', 'tombe',
                              'tombeau', 'torture', 'tranquille',
                              'transi', 'trépas', 'trépassé',
                              'tué', 'usé', 'victime', 'vidé']],
                 'Joie': [0, ['agrément', 'allégresse', 'amusement', 'épanouissement', 'ardeur', 'avantage',
                              'béatitude', 'bien', 'être', 'bienfait', 'bonheur', 'consolation', 'contentement',
                              'délice', 'douceur', 'enchantement', 'enjouement', 'enthousiasme', 'entrain',
                              'euphorie', 'exaltation', 'extase', 'exultation', 'félicité', 'fierté',
                              'folichonnerie', 'gaieté', 'gaité', 'griserie', 'hilarité', 'ivresse', 'jouissance',
                              'liesse', 'plaisir', 'régal', 'réjouissance', 'ravissement', 'rayonnement',
                              'rigolade', 'satisfaction', 'sourire', 'transport']],
                 'Triste':[0, ['abattu',
                          'accablé',
                          'accablant',
                          'affecté',
                          'affligé',
                          'affligeant',
                          'affreux',
                          'élégiaque',
                          'amer',
                          'émouvant',
                          'anéanti',
                          'angoissant',
                          'éploré',
                          'assombri',
                          'éteignoir',
                          'atrabilaire',
                          'attendrissant',
                          'atterré',
                          'attristé',
                          'attristant',
                          'austère',
                          'bileux',
                          'bilieux',
                          'bouleversant',
                          'brumeux',
                          'cafardeux',
                          'calamiteux',
                          'catastrophique',
                          'chagrin',
                          'chagriné',
                          'consterné',
                          'constipé',
                          'cruel',
                          'déchirant',
                          'découragé',
                          'décourageant',
                          'défait',
                          'déplorable',
                          'déprimé',
                          'désabusé',
                          'désenchanté',
                          'désespéré',
                          'désolé',
                          'douloureux',
                          'dramatique',
                          'ennuyeux',
                          'fâcheux',
                          'funèbre',
                          'funeste',
                          'grave',
                          'inconsolable',
                          'infortuné',
                          'lamentable',
                          'lugubre',
                          'médiocre',
                          'mélancolique',
                          'malheureux',
                          'maussade',
                          'mauvais',
                          'minable',
                          'misérable',
                          'moche',
                          'monotone',
                          'morne',
                          'morose',
                          'navré',
                          'navrant',
                          'neurasthénique',
                          'nostalgique',
                          'obscur',
                          'pauvre',
                          'peiné',
                          'piètre',
                          'piteux',
                          'pitoyable',
                          'rabat', 'joie',
                          'regrettable',
                          'rembruni',
                          'renfrogné',
                          'romantique',
                          'rude',
                          'sépulcral',
                          'saturnien',
                          'sauvage',
                          'sévère',
                          'sempiternel',
                          'sinistre',
                          'sombre',
                          'soucieux',
                          'sourcilleux',
                          'taciturne',
                          'ténébreux',
                          'tendu',
                          'terne',
                          'torturant',
                          'tragique',
                          'trouble',
                          'fête']],
                 'Colère':  [0,
                            ['ébullition', 'agité', 'agitation', 'agressif', 'agressivité', 'aigreur', 'algarade',
                             'animosité', 'éréthisme', 'atrabilaire', 'atrabile', 'bile', 'bilieux', 'bouffée',
                             'bourrasque', 'chagrin', 'colérique', 'courroucé', 'courroux', 'crise',
                             'déchaînement', 'dépit', 'effervescence', 'emportement', 'exaspéré', 'exaspération',
                             'excitation', 'explosion', 'fâcherie', 'feu', 'foudre', 'fulminant', 'fureur',
                             'furie', 'furieux', 'grogne', 'haine', 'hargne', 'hargneux', 'humeur', 'impatience',
                             'impatient', 'indignation', 'irascibilité', 'ire', 'irrité', 'irritabilité',
                             'irritable', 'mécontentement', 'monté', 'péché', 'querelle', 'rage', 'rageur',
                             'rancoeur', 'représailles', 'ressentiment', 'rogne', 'scène', 'surexcitation',
                             'susceptibilité', 'tempête', 'vengeance', 'violence']]}
        compteur = 0# On crée un compteur
        L = []
        for i in theme.keys():
            theme[i][0] = 0 # on initialise chaque mot a 0
        for i in theme.keys(): #on parcour le dico theme pour chaque cle de se dernier
            for v in theme[i][1]:
                p = boyer_moore(texte, v) # on fait boyermoore pour chaque texte avec chaque mot des listes dans le dico
                theme[i][0] += len(p)

                compteur += len(p) # On ajoute a notre compteur la longueur de p
            L.append(theme[i][0])
        Max = maxi(L)
        for i in theme.keys():
            if theme[i][0] == Max:
                return  [compteur, theme[i][0], i]

    def afficher(texte, screen):
        compteur = get_info(texte)[0]
        theme = get_info(texte)[1]
        if get_info(texte)[0] != 0:
            th = pygame.font.Font("police.ttf", 20)
            th = th.render(str(get_info(texte)[2]), True, pygame.Color("#000000"))
        return th

    th = police.render('',True, (0, 0, 0))
    running = True
    while running:
        screen.blit(fond, (0, 0))
        screen.blit(Q, Q_rect)
        screen.blit(r, r_rect)
        screen.blit(texte, texte_rect)
        screen.blit(texte2, texte2_rect)
        screen.blit(th, (350, 475))

        v = pygame.event.get()
        for event in v:  # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                running = False  # running est sur False
                sys.exit()  # pour fermer correctement
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Q_rect.collidepoint(event.pos):  # Bouton qui permet de revenir au menu
                    menu()
                if r_rect.collidepoint(event.pos): #Bouton qui permet de lancer Boyer-moore
                    get_info(paroles)
                    th = afficher(paroles, screen)
        pygame.display.update()  # pour ajouter tout changement à l'écran


def lancer():
    """Fonction qui permet de lancer le programme de scraping et de boyer-moore"""
    # Création de la musique
    pygame.mixer.music.load("musique.mp3")
    son = pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    #Création de la fenetre de base
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Scrap")

    # Fond
    fond = pygame.image.load("Back.jpg")
    fond = pygame.transform.scale(fond, (800, 600))

    #Bouton quitter
    Q = pygame.image.load("Quitter.png").convert_alpha()
    Q = pygame.transform.scale(Q, (50, 50))
    Q_rect = Q.get_rect()
    Q_rect.x = 740
    Q_rect.y = 540

    #Bouton lancement de la recherche
    r = pygame.image.load("Rechercher.png").convert_alpha()
    r = pygame.transform.scale(r, (75, 75))
    r_rect = r.get_rect()
    r_rect.x=350
    r_rect.y=330

    # logo du menu
    st = pygame.image.load("st.png").convert_alpha()
    st = pygame.transform.scale(st, (300, 300))
    st_rect = st.get_rect()
    st_rect.x = 240
    st_rect.y = 5

    # Artiste  :
    Art = pygame.image.load("Art.png").convert_alpha()
    Art = pygame.transform.scale(Art, (180, 180))
    Art_rect = Art.get_rect()
    Art_rect.x = 80
    Art_rect.y = 178

    # Chanson :
    Chan = pygame.image.load("Chan.png").convert_alpha()
    Chan = pygame.transform.scale(Chan, (180, 180))
    Chan_rect = Chan.get_rect()
    Chan_rect.x = 525
    Chan_rect.y = 182

    police = pygame.font.Font("police.ttf", 12)
    info1 = police.render("*Scraping sur Parole.net", True, pygame.Color("#000000"))
    info1_rect = info1.get_rect()
    info1_rect.x, info1_rect.y = 5, 585

    # Création du rectangle pour écrire
    rec1 = rectangle(220, 250, 150, 30, color=(255, 255, 255), cornerradius=1)
    rec2 = rectangle(400, 250, 150, 30, color=(255, 255, 255), cornerradius=1)

    #Instance de textentry
    text1 = TextEntry(screen, (255, 255, 255), (220, 250, 150, 30), "text", sizetxt=15)
    text2 = TextEntry(screen, (255, 255, 255), (400, 250, 150, 30), "text", sizetxt=15)

    #Fonction scrapping
    def scrap(name, chanson):
        sauce1 = urllib.request.urlopen(f"https://www.paroles.net/{name}/paroles-{chanson}")
        print(f"https://www.paroles.net/{name}/paroles-{chanson}")
        soup1 = bs.BeautifulSoup(sauce1,'html5lib')
        fichier = open('chanson.txt', 'w')
        tmp = soup1.find('div', attrs={"class": "song-text"}).text
        fichier.write(tmp)
        fichier.close()

    running = True
    while running :
        screen.blit(fond,(0,0))
        screen.blit(Q,Q_rect)
        screen.blit(r,r_rect)
        screen.blit(st, st_rect)
        screen.blit(Art , Art_rect)
        screen.blit(Chan, Chan_rect)
        screen.blit(info1, info1_rect)
        rec1.iblit(screen)
        rec2.iblit(screen)
        v = pygame.event.get()
        name = ""
        chanson = ""
        for event in v:  # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                running = False  # running est sur False
                sys.exit()  # pour fermer correctement
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Q_rect.collidepoint(event.pos):  # Bouton qui permet de revenir au menu
                    menu()
                if text1.get_text() != "" and text2.get_text() != "":
                    if r_rect.collidepoint(event.pos):#Bouton recherche la musique
                        name = text1.get_text().lower().strip()
                        chanson = text2.get_text().lower().strip()
                        scrap(name, chanson)

        text1.afficher(v)
        text2.afficher(v)


        pygame.display.update()  # pour ajouter tout changement à l'écran


def menu():
    """Fonction qui crée le menu"""
    pygame.init()
    continuer = True

    # Création de la musique
    pygame.mixer.music.load("musique.mp3")
    son = pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    # Création de la fenetre de base
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Scrap")

    # Fond
    fond = pygame.image.load("Back.jpg")
    fond = pygame.transform.scale(fond, (800, 600))

    # Bouton quitter
    Q = pygame.image.load("Quitter.png").convert_alpha()
    Q = pygame.transform.scale(Q, (50, 50))
    Q_rect = Q.get_rect()
    Q_rect.x = 740
    Q_rect.y = 540

    #Bouton lancer
    l = pygame.image.load("Scrap.png").convert_alpha()
    l = pygame.transform.scale(l, (155, 155))
    l_rect = l.get_rect()
    l_rect.x = 310
    l_rect.y = 250

    # logo du menu
    st = pygame.image.load("st.png").convert_alpha()
    st = pygame.transform.scale(st, (300, 300))
    st_rect = st.get_rect()
    st_rect.x = 240
    st_rect.y = 5

    # Bouton Boyer-moore
    bo = pygame.image.load("Boyer.png").convert_alpha()
    bo = pygame.transform.scale(bo, (225, 225))
    bo_rect = bo.get_rect()
    bo_rect.x = 267
    bo_rect.y = 340

    while continuer:
        screen.blit(fond,(0,0))
        screen.blit(Q,Q_rect)
        screen.blit(l, l_rect)
        screen.blit(st, st_rect)
        screen.blit(bo , bo_rect)
        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                running = False  # running est sur False
                sys.exit()  # pour fermer correctement
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verif si la souris touche le bouton
                if l_rect.collidepoint(event.pos):
                    # Le jeux en mode True
                    lancer()
                if Q_rect.collidepoint(event.pos):  # Bouton qui permet de quitter le jeux
                    pygame.quit()
                if bo_rect.collidepoint(event.pos):
                    boyermoore()
        # Affichage des elements
        pygame.display.update()
menu()


