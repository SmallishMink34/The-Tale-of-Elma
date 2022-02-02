import pygame, pytmx, pyscroll

class Map:
    def __init__(self, name, walls:list[pygame.Rect], objecte, group, tmx_data):
        self.name = name
        self.walls = walls
        self.object = objecte
        self.group = group
        self.tmx_data =  tmx_data

class Mapmanager:
    def __init__(self, screen, player):
        self.maps = {}
        self.current_map = "Grotte"
        self.screen = screen
        self.player = player

        self.register_map("Lobby", 8)
        self.register_map("Grotte")

        self.teleport_player("PlayerPos")

    def register_map(self, name, player_layer=7):
        self.tmx = pytmx.util_pygame.load_pygame(f"img/tile/{name}.tmx")
        mapdata = pyscroll.data.TiledMapData(self.tmx)
        map_layer = pyscroll.orthographic.BufferedRenderer(mapdata, self.screen.get_size())
        map_layer.zoom = 1.6

        self.walls = []
        self.objects_input = {}

        for obj in self.tmx.objects:  # Ajout des collsion dans des listes
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "InputAction":
                self.objects_input[obj.name] = [obj, pygame.Rect(obj.x, obj.y, obj.width, obj.height), "InputAction"]

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,
                                            default_layer=player_layer)  # groupe contenant le joueur et la map
        self.group.add(self.player)

        self.maps[name] = Map(name, self.walls, self.objects_input,self.group, self.tmx)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_objectinp(self, type, returntype="all"):
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

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

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

    def collision(self):
        for i in self.get_group().sprites():
            if i.feet.collidelist(self.get_walls()) > -1:  # si les pieds du joueurs entre en collision avec un objet
                i.moveback()
            for element in self.get_objectinp("InputAction", "all"):
                if i.rect.colliderect(element[1]):  # si le joueurs entre en collision avec un objet
                    i.inputaction(element[0])