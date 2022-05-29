
import pygame, pytmx, pyscroll
import mapscript
import transition
import ClassPG as PG
import valeurs
import Ennemis
import random
import fight


class Map:
    def __init__(self, name, walls, objecte, group, tmx_data, mapdata, mapobject, ennemis=[]):
        self.name = name
        self.walls = walls
        self.object = objecte
        self.group = group
        self.tmx_data = tmx_data
        self.map_data = mapdata
        self.mapobject = mapobject
        self.ennemis = ennemis


class Tuile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tile_size):
        super(Tuile, self).__init__()
        self.name = "tile"
        self.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        self.image = image
        self.type = "tile"


class Mapmanager:
    def __init__(self, screen, player):
        self.mapobject = None
        self.maps = {}
        self.basemap = "Lobby"
        self.load_localtion()
        self.current_map = self.basemap
        self.screen = screen
        self.player = player

        self.loading = False  # Load from the file
        self.seecollision = False
        self.register_map("Lobby", mapscript.lobby(self))
        self.register_map("Grotte", mapscript.Grotte(self))
        self.register_map("Village", mapscript.Village(self))
        self.register_map("Maison", mapscript.Maison(self))
        self.register_map("Puit", mapscript.Puit(self))
        self.register_map("Foret", mapscript.Foret(self))
        self.register_map("Maison_Foret", mapscript.Maison_Foret(self))
        self.register_map("Plaine", mapscript.Plaine(self))
        self.register_map("MaisonPêcheur", mapscript.MaisonPêcheur(self))
        self.register_map("Plage", mapscript.Plage(self))
        self.register_map("MaisonPlage", mapscript.MaisonPlage(self))

        self.current_map = self.basemap

        self.changemap(self.basemap, "PlayerPos")

        self.Animation = transition.Animation(3)

        self.song = {}
        self.song['door'] = PG.son("../song/Ingame/door.mp3", "song")
        self.song['chest'] = PG.son("../song/Ingame/chest.mp3", "song")
        self.song['aie'] = PG.son("../song/Ingame/aie.mp3", "song")

        self.teleport_player("PlayerPos")

    def alltiles(self):
        self.alltiles_d = {}
        self.alltiles_d["Base"] = pytmx.util_pygame.load_pygame("../img/tile/alltiles.tmx", load_all_tiles=True)
        self.alltiles_d["Base2"] = pytmx.util_pygame.load_pygame("../img/tile/Base2Tiles.tmx", load_all_tiles=True)
        self.alltiles_d["Base3"] = pytmx.util_pygame.load_pygame("../img/tile/TX Props.tmx", load_all_tiles=True)

    def register_map(self, name, mapobject):
        self.current_map = name
        tmx = pytmx.util_pygame.load_pygame(f"../img/tile/{name}.tmx", load_all_tiles=True)
        self.alltiles()
        mapdata = pyscroll.data.TiledMapData(tmx)
        map_layer = pyscroll.orthographic.BufferedRenderer(mapdata, self.screen.get_size())
        map_layer.zoom = 1.6 * (self.screen.get_size()[0] / 1280)
        self.walls = []
        objects_input = {}

        player_layer = tmx.layers
        liste = []
        for element in range(len(player_layer)):
            liste.append(player_layer[element].name)
            if player_layer[element].name == "PlayerCalque":
                u = element
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=int(u))

        for obj in tmx.objects:  # Ajout des collsion dans des listes
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if self.seecollision: group.add(
                    PG.img("../img/menu/background.jpg", obj.x, obj.y, obj.width, obj.height, False))
            if obj.type != "Collision":
                objects_input[obj.id] = [obj, pygame.Rect(obj.x, obj.y, obj.width, obj.height), obj.type]
                if self.seecollision: group.add(
                    PG.img("../img/img.inv/case.png", obj.x, obj.y, obj.width, obj.height, False))

                # Créer un nombre aléatoire d'ennemis dans un emplacement aléatoire dans une zone donnée et les ajoutes dans le group de la map.
        ennemis = []
        for element in tmx.objects:
            if element.type == "Ennemi":
                for i in range(element.properties['nbennemis']):
                    id = int(random.choice(element.properties['Ennemis'].split(",")))
                    lvl = random.randint(int(element.properties['level'].split(",")[0]),
                                         int(element.properties['level'].split(",")[-1]))
                    x = int(random.randint(int(element.x), int(element.x + element.width)))
                    y = int(random.randint(int(element.y), int(element.y + element.height)))
                    a = Ennemis.Ennemy(id, lvl, x, y)
                    group.add(a)
                    ennemis.append(a)


        # groupe contenant le joueur et la map
        group.add(self.player)
        group.change_layer(self.player, u)

        self.maps[name] = Map(name, self.walls, objects_input, group, tmx, mapdata, mapobject, ennemis)
        mapobject.load()
        self.actionnb = mapobject.actionb


    def reloadmap(self):

        self.maps[self.current_map].map_layer.reload()
        self.maps[self.current_map].map_layer.set_size((1280, 720))

        pygame.display.flip()

    def zoomIO(self, level):
        self.maps[self.current_map].zoom = level

    def save_all(self, name):
        self.maps[name].allmap.save_player_info()

    def save(self, name):
        """
        Il écrit la carte actuelle et le dictionnaire actionb dans un fichier

        :param name: Le nom du fichier de sauvegarde
        """
        print("savegarde de la map : ", name)
        w = open(valeurs.valeur.save_l + f"/save/{name}.txt", "w")
        w.write(self.current_map + "\n")

        for i in self.maps[self.current_map].mapobject.actionb.keys():
            w.write(str(i) + ": " + str(self.maps[self.current_map].mapobject.actionb[i]) + "\n")
        w.close()

    def load(self, name):
        try:
            w = open(valeurs.valeur.save_l + f"/save/{name}.txt", "r")
        except FileNotFoundError:
            open(valeurs.valeur.save_l + f"/save/{name}.txt", "w")
            w = open(valeurs.valeur.save_l + f"/save/{name}.txt", "r")
        liste = w.readlines()
        a = {}
        for i in liste:
            try:
                a[i.split(":")[0]] = eval(i.split(":")[1])
            except IndexError:
                pass

        if a != {}:
            return a
        else:
            return None

    def load_localtion(self):
        """ Fonction qui change la location du spawnpoint"""
        a = open(valeurs.valeur.save_l + "/save/sauvegarde.txt", "r")
        liste = a.readlines()
        try:
            self.basemap = liste[0].split(": ")[1].strip()
        except IndexError:
            self.basemap = "Lobby"
        return self.basemap

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_objectinp(self, type, returntype="all"):
        """
        Fonction qui renvoie une liste qui renvoie les objet d'un certain type
        """
        l = []
        if returntype == "rect":
            for i in self.get_map().object.keys():
                if self.get_map().object[i][2] == type:
                    l.append(self.get_map().object[i][1])
        if returntype == "object":
            for i in self.get_map().object.keys():
                if self.get_map().object[i][2] == type:
                    l.append(self.get_map().object[i][0])
        if returntype == "all":
            for i in self.get_map().object.keys():
                if self.get_map().object[i][2] == type:
                    l.append(self.get_map().object[i])
        return l

    def get_allobject(self, returntype="all"):
        """
        Fonction qui renvoie tout les objects
        :param returntype:
        :return:
            returntype = rect : return pygame.Rect
            returntype = object : return object
            returntype = all : [object, pygame.Rect]
        """
        l = []
        if returntype == "rect":
            for i in self.get_map().object.keys():
                l.append(self.get_map().object[i][1])
        if returntype == "object":
            for i in self.get_map().object.keys():
                l.append(self.get_map().object[i][0])
        if returntype == "all":
            for i in self.get_map().object.keys():
                l.append(self.get_map().object[i])
        return l

    def get_object(self, id):
        return self.get_map().tmx_data.get_object_by_name(id)

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.rect.centerx, self.player.rect.centery = point.x, point.y
        self.player.save_old_location()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def updating(self):
        self.maps[self.current_map].group.update()
        self.collision()

        try:
            self.maps[self.current_map].mapobject.update()
        except KeyError:
            pass

    def collision(self):
        for i in self.get_group().sprites():
            if i.type == 'Joueur':
                if i.feet.collidelist(
                        self.get_walls()) > -1:  # si les pieds du joueurs entre en collision avec un objet
                    i.moveback()
                player = i
                self.maps[self.current_map].mapobject.collision(i)

        for i3 in self.maps[self.current_map].ennemis:
            if i3.rect.colliderect(player.rect):
                fightt = fight.fight(self.player, i3.id,i3.lvl)
                fightt.image(self.screen)
                self.player.allinputoff(False)
                if fightt.FightScreen() in ["Player", "Fuite"]:
                    self.maps[self.current_map].ennemis.remove(i3)
                    self.get_group().remove(i3)
                else:
                    self.teleport_player("PlayerPos")
                    self.player.hp = self.player.hpmax
                self.player.allinputoff(True)
                self.player.pressed[pygame.K_l] = False

    def checkcollision(self, x, y):
        for element in self.get_walls():
            if element.collidepoint((x, y)):
                return True

    def changemap(self, name, teleportpoint):
        """
        Change la map actuel
        :param name: str
        :param teleportpoint: str
        :return: Nothing
        """
        self.current_map = name
        self.mapobject = self.maps[name].mapobject
        self.teleport_player(teleportpoint)


    def remove_collision(self, obj):
        self.maps[self.current_map].walls.remove(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    """def remove_inputaction(self, obj):
        self.maps[self.current_map].object"""

    def add_collision_from_obj(self, obj):
        self.maps[self.current_map].walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def add_collision_from_rect(self, rect):
        self.maps[self.current_map].walls.append(rect)

    def add_image_to_draw(self, file, x, y, w, h):
        img = PG.img(file, x, y, w, h, True)
        self.maps[self.current_map].group.add(img)

    def add_element_to_draw_obj(self, name: str, gid: int, x: int, y: int, layer: int):
        img = self.alltiles_d[name].get_tile_image_by_gid(gid + 1)
        self.maps[self.current_map].group.add(Tuile(x, y, img, 32), layer=layer)

    def add_class_to_draw_obj(self, object):
        self.maps[self.current_map].group

    def remove_element_to_draw_obj(self, x, y):
        try:
            for element in self.maps[self.current_map].group:
                if element.name == "tile":
                    if element.rect.x == x * 32 and element.rect.y == y * 32:
                        self.maps[self.current_map].group.remove(element)
        except AttributeError:
            pass

    def set_layer_visible(self, layer, Visible):
        """
        Met le layer en visible ou non
        :param layer: str
        :param Visible: bool
        :return: Nothing
        """
        self.maps[self.current_map].tmx_data.get_layer_by_name(layer).visible = Visible

    def get_layer_by_name(self, name):
        return self.get_map().tmx_data.get_layer_by_name(name)

