import pygame, pytmx, pyscroll


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
        self.current_map = "Grotte"
        self.screen = screen
        self.player = player

        self.register_map("Lobby", 8)
        self.register_map("Grotte")

        self.teleport_player("PlayerPos")

    def register_map(self, name, player_layer=7):
        self.tmx = pytmx.util_pygame.load_pygame(f"../img/tile/{name}.tmx")
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

        self.maps[name] = Map(name, self.walls, self.objects_input, self.group, self.tmx, mapdata)

        self.actionnb = {"Pont": 0, "Chest": False}

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

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

        if self.get_object("Pont").properties['Enable']:
            if self.actionnb['Pont'] == 5:
                self.get_object("Pont").properties['Enable'] = False

            if not self.get_object("Pont").properties['Enable']:
                self.remove_collision(self.get_object("Pont"))
                self.set_layer_visible('Pont', True)

    def collision(self):
        for i in self.get_group().sprites():
            if i.type == 'Joueur':
                if i.feet.collidelist(self.get_walls()) > -1:  # si les pieds du joueurs entre en collision avec un objet
                    i.moveback()
                for element in self.get_objectinp("InputAction", "all"):
                    if i.feet.colliderect(
                            element[1]) and self.player.inputaction():  # si le joueurs entre en collision avec un objet
                        if "Portail" in element[0].name:  # Si c'est un point de teleportation
                            try:
                                var = element[0].properties['To?']
                            except KeyError:
                                var = self.current_map

                            try:
                                var2 = element[0].properties['TeleportPoint']
                            except KeyError:
                                var2 = 'PlayerPos'

                            self.changemap(var, var2)
                        if "Panneau" in element[0].name:
                            self.player.gui.DialogP(element[0].properties['Speaker'], element[0].properties['Texte'])
                        if "Torch" in element[0].name:
                            if not element[0].properties['Infire']:
                                element[0].properties['Infire'] = True
                                self.actionnb['Pont'] += 1
                                self.add_element_to_draw_obj(8, element[0].x, element[0].y)
                                print(self.actionnb['Pont'])

                        else:
                            print(element[0].name)

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
