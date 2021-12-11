import pygame
import ClassPG as PG

#class du menu
menu = PG.game("FluoFloat", (1280,720), 60) # <- Nom de test

# Dico element a afficher

d = {}

#Class dans le menu
d['Texte'] = PG.Texte("FluoFloat", 640, 120, True, (255,255,255), 70)
d['Play'] = PG.Texte("Play", 640, 220, True, (255,255,255), 36)

for i in d.keys():
    menu.ielement.append(d[i])

while menu.running:
    menu.gameloop()

    menu.eventpy()

    menu.iblitall()