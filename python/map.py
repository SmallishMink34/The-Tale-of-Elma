import pygame, pytmx, pyscroll
import mapscript
import transition
import ClassPG as PG

class Map:
    def __init__(self, name, walls: list[pygame.Rect], objecte, group, tmx_data, mapdata, mapobject):
        self.name = name
        self.walls = walls
        self.object = objecte
        self.group = group
        self.tmx_data = tmx_data
        self.map_data = mapdata
        self.mapobject = mapobject


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
        self.basemap = "Village"
        self.load_localtion()
        self.current_map = self.basemap
        self.screen = screen
        self.player = player

        self.loading = False  # Load from the file
        self.seecollision = False
        self.register_map("Lobby", mapscript.lobby(self))
        self.register_map("Grotte", mapscript.Grotte(self))
        self.register_map("Village", mapscript.Village(self))

        self.changemap(self.basemap, "PlayerPos")

        self.Animation = transition.Animation(3)



        self.teleport_player("PlayerPos")

    def alltiles(self):
        self.alltiles_d = {}
        self.alltiles_d["Base"] = pytmx.util_pygame.load_pygame("../img/tile/alltiles.tmx", load_all_tiles=True)
        self.alltiles_d["Base2"] = pytmx.util_pygame.load_pygame("../img/tile/Base2Tiles.tmx", load_all_tiles=True)
        self.alltiles_d["Base3"] = pytmx.util_pygame.load_pygame("../img/tile/TX Props.tmx", load_all_tiles=True)

    def register_map(self, name, mapobject):
        self.current_map = name
        self.tmx = pytmx.util_pygame.load_pygame(f"../img/tile/{name}.tmx", load_all_tiles=True)
        self.alltiles()
        self.mapdata = pyscroll.data.TiledMapData(self.tmx)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.mapdata, self.screen.get_size())
        self.map_layer.zoom = 1.6 * (self.screen.get_size()[0] / 1280)
        self.walls = []
        self.objects_input = {}

        player_layer = self.tmx.layers
        for element in range(len(player_layer)):
            if player_layer[element].name == "PlayerCalque":
                u = element
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                            default_layer=u)

        for obj in self.tmx.objects:  # Ajout des collsion dans des listes
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if self.seecollision:self.group.add(PG.img("../img/menu/background.jpg", obj.x, obj.y, obj.width, obj.height, False))
            if obj.type != "Collision":
                self.objects_input[obj.name] = [obj, pygame.Rect(obj.x, obj.y, obj.width, obj.height), obj.type]

          # groupe contenant le joueur et la map
        self.group.add(self.player)
        self.maps[name] = Map(name, self.walls, self.objects_input, self.group, self.tmx, self.mapdata, mapobject)
        self.mapobject = mapobject
        mapobject.load()
        self.actionnb = mapobject.actionb
        self.current_map = self.basemap

    def reloadmap(self):
        print('reload de la map')

        self.map_layer.reload()
        self.map_layer.set_size((1280, 720))

        pygame.display.flip()

    def zoomIO(self, level):
        self.map_layer.zoom = level

    def save(self, name):
        w = open(f"save/{name}.txt", "w")
        w.write(self.current_map + "\n")

        for i in self.maps[self.current_map].mapobject.actionb.keys():
            w.write(str(i) + ": " + str(self.maps[self.current_map].mapobject.actionb[i]) + "\n")
        w.close()

    def load(self, name):
        try:
            w = open(f"save/{name}.txt", "r")
        except FileNotFoundError:
            open(f"save/{name}.txt", "w")
            w = open(f"save/{name}.txt", "r")
        liste = w.readlines()
        a = {}
        for i in liste:
            try:
                a[i.split(":")[0]] = eval(i.split(":")[1])
            except IndexError:
                pass

        if a != {}:return a
        else: return None

    def load_localtion(self):
        """ Fonction qui change la location du spawnpoint"""
        a = open("save/spawnpoint.txt", "r")
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

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.rect.centerx, self.player.rect.centery = point.x, point.y
        self.player.save_old_location()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def updating(self):
        self.group.update()
        self.collision()

        try:
            self.mapobject.update()
        except KeyError:
            pass

    def collision(self):
        for i in self.get_group().sprites():
            if i.type == 'Joueur':
                if i.feet.collidelist(
                        self.get_walls()) > -1:  # si les pieds du joueurs entre en collision avec un objet
                    i.moveback()
                self.mapobject.collision(i)

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

    def add_collision_from_obj(self, obj):
        self.maps[self.current_map].walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def add_collision_from_rect(self, rect):
        self.maps[self.current_map].walls.append(rect)

    def add_element_to_draw_obj(self, name: str, gid: int, x: int, y: int, layer: int):
        img = self.alltiles_d[name].get_tile_image_by_gid(gid + 1)
        self.maps[self.current_map].group.add(Tuile(x, y, img, 32), layer=layer)

    def remove_element_to_draw_obj(self, x, y):
        for element in self.maps[self.current_map].group:
            if element.name == "tile":
                if element.rect.x == x * 32 and element.rect.y == y * 32:
                    self.maps[self.current_map].group.remove(element)

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
