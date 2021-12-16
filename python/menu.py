import pygame
import ClassPG as PG

def menu():
    #class du menu
    menu = PG.game("FluoFloat", (1280,720), 60) # <- Nom de test

    # Dico element a afficher

    d = {}

    #Class dans le menu
    d['Texte'] = PG.Texte("FluoFloat", menu.w/2, 120, True, (255,255,255), 70, (255,255,255))
    d['Play'] = PG.Texte("Ply", menu.w/2, 220, True, (255,255,255), 36)
    d['Option'] = PG.Texte("Option", menu.w/2, 280, True, (255,255,255), 36)
    d['Credits'] = PG.Texte("Credis", menu.w/2, 340, True, (255,255,255), 36)
    d['Exit'] = PG.Texte("Exit", menu.w/2, 400, True, (255,255,255), 36)

    for i in d.keys():
        menu.telement.append(d[i])

    while menu.running:
        menu.gameloop()

        menu.eventpy()

        menu.iblitall()

menu()