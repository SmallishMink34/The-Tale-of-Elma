import pygame, pytmx, pyscroll
import mapscript

class Map:
    def __init__(self, name, walls: list[pygame.Rect], objecte, group, tmx_data, mapdata):
        self.name = name
        self.walls = walls
        self.object = objecte
        self.group = group
        self.tmx_data = tmx_data
        self.map_data = mapdata


class Tuile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        self.image = image
        self.type = "tile"

class Mapmanager:
    def __init__(self, screen, player):
        self.maps = {}
        self.current_map = "Lobby"
        self.screen = screen
        self.player = player

        self.register_map("Lobby", mapscript.lobby(self), 8)
        self.register_map("Grotte", mapscript.Grotte(self))

        self.teleport_player("PlayerPos")

    def register_map(self, name, mapobject,player_layer=7):
        self.tmx = pytmx.util_pygame.load_pygame(f"../img/tile/{name}.tmx")
        mapdata = pyscroll.data.TiledMapData(self.tmx)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(mapdata, self.screen.get_size())
        self.map_layer.zoom = 1.6
        self.walls = []
        self.objects_input = {}

        for obj in self.tmx.objects:  # Ajout des collsion dans des listes
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "InputAction":
                self.objects_input[obj.name] = [obj, pygame.Rect(obj.x, obj.y, obj.width, obj.height), "InputAction"]

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer,
                                            default_layer=player_layer)  # groupe contenant le joueur et la map
        self.group.add(self.player)

        self.maps[name] = Map(name, self.walls, self.objects_input, self.group, self.tmx, mapdata)
        self.mapobject = mapobject
        self.actionnb = mapobject.actionb

    def reloadmap(self):
        print('reload de la map')

        self.map_layer.reload()
        self.map_layer.set_size((1280, 720))
        
        pygame.display.flip()
        

    def zoomIO(self, level):
        self.map_layer.zoom = level

    def save(self):
        w = open("save/save.txt", "w")
        w.write(self.current_map+"\n")

        for i in self.actionnb.keys():
            w.write(str(i)+ ": "+ str(self.actionnb[i])+"\n")
        w.close()

    def load(self):
        w = open("save/save.txt", "r")
        liste = w.readlines()
        a = {}
        for i in liste:
            try: 
                a[i.split(":")[0]] = eval(i.split(":")[1])
            except IndexError:
                pass
        print(a)
        return a
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

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.rect.x, self.player.rect.y = point.x, point.y
        self.player.save_old_location()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def updating(self):
        self.group.update()
        self.collision()

        try :
            self.mapobject.update()
        except KeyError:
            pass

    def collision(self):
        for i in self.get_group().sprites():
            if i.type == 'Joueur':
                if i.feet.collidelist(self.get_walls()) > -1:  # si les pieds du joueurs entre en collision avec un objet
                    i.moveback()
                self.mapobject.collision(i)              

    def checkcollision(self, x, y):
        for element in self.get_walls():
            if element.collidepoint((x, y)):
                print('Il y a un obstacle')
                return True

    def changemap(self, name, teleportpoint):
        self.current_map = name
        self.teleport_player(teleportpoint)

    def remove_collision(self, obj):
        self.walls.remove(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def add_collision_from_obj(self, obj):
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def add_collision_from_rect(self, rect):
        self.walls.append(rect)

    def add_element_to_draw_obj(self, gid, x, y):
        image = self.maps[self.current_map].tmx_data.get_tile_image_by_gid(gid)
        self.group.add(Tuile(x, y, image, 32))
        print(x, y)

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