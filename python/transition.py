import pygame
import ClassPG as PG
import valeurs


class Animation:
    def __init__(self,speed=1, loop=1):
        self.speed = speed
        self.loop = loop
        self.isrunning = False
        self.switch = False

        self.anim = {"fade_in": fade_in("fade_in", "reverse"), "fade_out": fade_in("fade_out", "normal")}

        full = pygame.FULLSCREEN if valeurs.valeur.toggle else 0
        self.screen = pygame.display.set_mode(valeurs.valeur.screensize, full)

    def one_by_one_iblit(self, screen, name):
        self.name = name
        self.runn(screen)

    def runn(self, screen):
        pygame.image.save(screen, "../img/temp/screene.png")
        print('photo')
        self.a = PG.img("../img/temp/screene.png", 0, 0, valeurs.valeur.screensize[0],
                        valeurs.valeur.screensize[1], False)
        self.i = 0
        self.isrunning = True
        while self.isrunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isrunning = False
            self.a.iblit(self.screen)

            self.anim[self.name].iblit(self.screen, int(self.i))
            self.i = self.i + 1 / self.speed
            if self.i < 0 or self.i > self.anim[self.name].number-1:
                print('run off')
                self.isrunning = False
            pygame.display.update()


class fade_in:
    def __init__(self, name, sens):
        self.name = name
        self.number = 60
        self.sens = sens
        self.d = {}
        for i in range(self.number):
            a = (5 - len(str(i))) * "0" + str(i)
            self.d[str(i)] = PG.img("../img/transition/fade/Fade_" + str(a) + ".png", 0, 0,
                                    valeurs.valeur.screensize[0], valeurs.valeur.screensize[1], False)

    def iblit(self, screen, i):
        i = i if self.sens == "normal" else 60-1 - i
        self.d[str(i)].iblit(screen)
