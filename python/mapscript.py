import pygame


class Grotte:
    def __init__(self, mapmanager, save_load=True):
        self.mm = mapmanager
        self.save = save_load
        if save_load:
            self.actionb = self.mm.load() if self.mm.load() != None else {"Pont": 0, "Door": True, "Torch1": False,
                                                                          "Torch2": False, "Torch3": False,
                                                                          "Torch4": False, "Torch5": False}
        else:
            self.actionb = {"Pont": 0, "Door": True}
        self.allmap = Allmap(self.mm)

    def load(self):
        self.opendoor()
        self.pont()
        self.load_tile_map()

    def __str__(self):
        return "la map actuel est Grotte"

    def load_tile_map(self):
        for element in self.mm.get_objectinp("InputAction", "all"):
            if "Torch" in element[0].name:
                if self.actionb[element[0].name]:
                    self.mm.add_element_to_draw_obj("Base", 177, element[0].properties['x1'],
                                                    element[0].properties['y1'], 19)
        for element in self.mm.get_objectinp("add", "all"):
            self.mm.add_element_to_draw_obj(element[0].properties["tilename"], element[0].properties["idtile"],
                                            int(element[0].x / 32), int(element[0].y / 32), 8)

    def pont(self):
        if self.actionb['Pont'] == 5:
            self.mm.get_object("Pont").properties['Enable'] = False

        if not self.mm.get_object("Pont").properties['Enable']:
            self.mm.remove_collision(self.mm.get_object("Pont"))
            self.mm.set_layer_visible('Pont', True)

    def opendoor(self):
        if not self.actionb["Door"]:
            try:
                self.mm.remove_collision(self.mm.get_object("ExitDoor"))
            except ValueError:
                pass
            self.mm.remove_element_to_draw_obj(85, 65)
            self.mm.remove_element_to_draw_obj(85, 64)

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type == "Damage":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
            if element[0].type == "InputAction":
                if i.feet.colliderect(element[1]) and self.mm.player.inputaction():
                    if self.allmap.hand(element) is False: break

                    if "Torch" in element[0].name:
                        if element[0].name not in self.actionb.keys():
                            self.actionb[element[0].name] = False
                        if not element[0].properties['Infire'] and not self.actionb[element[0].name]:
                            print("sa marche ?")
                            element[0].properties['Infire'] = True
                            self.actionb[element[0].name] = True
                            self.actionb['Pont'] += 1
                            self.mm.add_element_to_draw_obj("Base", 177, element[0].properties['x1'],
                                                            element[0].properties['y1'], 19)
                            self.pont()
                    if "Door" in element[0].name:
                        self.actionb["Door"] = False
                        self.opendoor()
                    self.allmap.collision(element)

    def update(self):
        pass


class lobby:
    def __init__(self, mapmanager, save_load=False):
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        if save_load:
            pass
        else:
            pass

        self.allmap = Allmap(self.mm)

    def load(self):
        pass

    def __str__(self):
        return "la map actuel est lobby"

    def collision(self, i):
        for element in self.mm.get_objectinp("InputAction", "all"):
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if i.feet.colliderect(element[1]) and self.mm.player.inputaction():
                    if self.allmap.hand(element) is False: break

                if "Portail" in element[0].name:  # Si c'est un point de teleportation
                    try:
                        var = element[0].properties['To?']
                    except KeyError:
                        var = self.mm.current_map
                    try:
                        var2 = element[0].properties['TeleportPoint']
                    except KeyError:
                        var2 = 'PlayerPos'

                    self.mm.changemap(var, var2)
                self.allmap.collision(element)

    def update(self):
        pass


class Village:
    def __init__(self, mapmanager, save_load=False):
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        if save_load:
            pass
        else:
            pass
        self.allmap = Allmap(self.mm)

    def load(self):
        pass

    def __str__(self):
        return "la map actuel est Village"

    def collision(self, i):
        for element in self.mm.get_objectinp("InputAction", "all"):
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if "Portail" in element[0].name:  # Si c'est un point de teleportation
                    try:
                        var = element[0].properties['To?']
                    except KeyError:
                        var = self.mm.current_map

                    try:
                        var2 = element[0].properties['TeleportPoint']
                    except KeyError:
                        var2 = 'PlayerPos'

                    self.mm.changemap(var, var2)
                self.allmap.collision(element)

    def update(self):
        pass


class Allmap():
    def __init__(self, mapmanager):
        self.mm = mapmanager

    def hand(self, element):
        try:
            if element[0].properties["needitem"] != 0:  # On regarde si on a besoin de la propriété needitem
                if self.mm.player.get_item_in_inventory(
                        5).obj is not None:  # On regarde que la main sois pas vide
                    if self.mm.player.get_item_in_inventory(5).obj.nom == element[0].properties[
                        "needitem"] and self.mm.player.get_item_in_inventory(5).obj.nbr >= \
                            element[0].properties[
                                "quantity"]:  # On regarde si c'est le bon objet et la bonne quantité
                        pass
                    else:
                        print('pas le bonne objet')
                        self.action_help(element)
                        return False
                else:
                    print('La main est vide')
                    return False
            else:
                print('Il na pas la propriété needitem')
                pass
        except (AttributeError, KeyError):
            print("Error")

    def collision(self, element):
        if "Chest" in element[0].name:
            self.mm.player.gui.inventory_chest(element[0].name)
        if "Panneau" in element[0].name:
            self.mm.player.gui.DialogP(element[0].properties['Speaker'], element[0].properties['Texte'])

        if "Portail" in element[0].name:  # Si c'est un point de teleportation
            try:
                var = element[0].properties['To?']
            except KeyError:
                var = self.mm.current_map

            try:
                var2 = element[0].properties['TeleportPoint']
            except KeyError:
                var2 = 'PlayerPos'
            self.mm.save()
            self.mm.changemap(var, var2)

    def action_help(self, element):
        if "help" in element[0].name:
            self.mm.player.gui.Mind(element[0].properties['Texte'])
            print("test")

    def collision_without_action(self, element):
        if "Spike" in element[0].name:
            print('Sa pique de : ', element[0].properties['Damage'])
