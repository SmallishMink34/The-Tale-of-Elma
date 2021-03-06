import pygame
import ClassPG as PG
import valeurs
import transition
import time
import Ennemis
import random
import inv


class Grotte:
    def __init__(self, mapmanager, save_load=True):
        self.name = "Grotte"
        self.mm = mapmanager
        self.save = save_load

        self.allmap = Allmap(self.mm, self)

    def default(self):
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(
            self.default()) else self.default()
        self.pont()
        self.load_tile_map()
        self.opendoor()
        self.allmap.load()

    def __str__(self):
        return "la map actuelle est Grotte"

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
            self.mm.remove_collision(self.mm.get_object("Ponte"))
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
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
            if element[0].type == "InputAction":
                if i.feet.colliderect(element[1]) and self.mm.player.inputaction():
                    if self.allmap.hand(element) is False: break

                    if "Torch" in element[0].name:
                        if element[0].name not in self.actionb.keys():
                            self.actionb[element[0].name] = False
                        if not element[0].properties['Infire'] and not self.actionb[element[0].name]:
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
        self.name = "Lobby"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        if save_load:
            pass
        else:
            pass

        self.allmap = Allmap(self.mm, self)

    def load(self):
        self.allmap.load()

    def __str__(self):
        return "la map actuel est lobby"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():
                if element[0].type != "InputAction":
                    if i.feet.colliderect(element[1]):
                        self.allmap.collision_without_action(element)
                # si le joueurs entre en collision avec un objet
                if i.feet.colliderect(element[1]) and self.mm.player.inputaction():
                    if self.allmap.hand(element) is False: break

                self.allmap.collision(element)

    def update(self):
        pass


class Village:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Village"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        self.allmap = Allmap(self.mm, self)

    def default(self):
        """
        Il renvoie un dictionnaire de tous les objets de la sc??ne, avec le nom de l'objet comme cl?? et la propri??t?? par
        d??faut de l'objet comme valeur
        :return: Dictionnaire de toutes les valeurs par d??faut de tous les objets du mod??le.
        """
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                print(i[0].name, i[0].properties["default"])
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(
            self.default()) else self.default()
        self.allmap.load()
        print(self.actionb)

    def __str__(self):
        return "la map actuel est Village"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if "puit" in element[0].name:
                    if self.actionb[element[0].name]:
                        self.allmap.collision(element)
                        break
                    self.actionb[element[0].name] = True
                if self.allmap.hand(element) is False: break
                if self.allmap.check_price(element) is False: break

                if "puit" in element[0].name:
                    self.actionb[element[0].name] = True
                self.allmap.collision(element)

    def update(self):
        pass


class Maison:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Maison"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}
        self.allmap = Allmap(self.mm, self)

    def load(self):

        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(
            self.default()) else self.default()
        self.load_img()
        self.allmap.load()

    def load_img(self):
        for element in self.mm.get_objectinp("InputAction", "all"):
            if "Pedestale" in element[0].name:
                if self.actionb[element[0].name]:
                    self.mm.add_image_to_draw(f"../img/item/{element[0].properties['needitem']}.png",
                                              int(element[0].properties['Itemx']), int(element[0].properties['Itemy']),
                                              32, 32)

    def default(self):
        """
        Il renvoie un dictionnaire de tous les objets de la sc??ne, avec le nom de l'objet comme cl?? et la propri??t?? par
        d??faut de l'objet comme valeur
        :return: Dictionnaire de toutes les valeurs par d??faut de tous les objets du mod??le.
        """
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def __str__(self):
        return "la map actuel est Maison"

    def collision(self, i):
        """
        La fonction v??rifie si le joueur entre en collision avec un objet, et si c'est le cas, elle v??rifie si le joueur
        appuie sur le bouton d'action

        :param i: le joueur
        """
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                self.allmap.collision(element)
                if element[0].name == "Game":
                    self.mm.player.gui.Game(self.mm.player.get_item_in_inventory(5).obj)
                if "Map" in element[0].name:
                    self.mm.player.gui.Carte(element[0].properties['Stage'])
                if "Pedestale" in element[0].name:
                    if not self.actionb[element[0].name]:
                        self.actionb[element[0].name] = True
                        self.mm.add_image_to_draw(f"../img/item/{element[0].properties['needitem']}.png",
                                                  int(element[0].properties['Itemx']),
                                                  int(element[0].properties['Itemy']), 32, 32)

    def update(self):
        pass


class Puit:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Puit"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}
        self.allmap = Allmap(self.mm, self)
        self.load()

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(self.default()) else self.default()
        self.allmap.load()

    def default(self):
        """
        Il renvoie un dictionnaire de tous les objets de la sc??ne, avec le nom de l'objet comme cl?? et la propri??t?? par
        d??faut de l'objet comme valeur
        :return: Dictionnaire de toutes les valeurs par d??faut de tous les objets du mod??le.
        """
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def __str__(self):
        return "la map actuel est Puit"

    def collision(self, i):
        """
        La fonction v??rifie si le joueur entre en collision avec un objet, et si c'est le cas, elle v??rifie si le joueur
        appuie sur le bouton d'action

        :param i: le joueur
        """
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                self.allmap.collision(element)

    def update(self):
        pass


class Foret:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Foret"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}
        self.allmap = Allmap(self.mm, self)

    def load_tile_map(self):
        for element in self.mm.get_objectinp("add", "all"):
            self.mm.add_element_to_draw_obj(element[0].properties["tilename"], element[0].properties["idtile"],
                                            int(element[0].x / 32), int(element[0].y / 32), 8)
    def default(self):
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load_arbre(self):
        self.a = PG.img(f"../img/grosarbre.png", 1870, 776, 150, 150)
        self.mm.maps[self.mm.current_map].group.add(self.a)

    def opendoor(self):
        if not self.actionb["Door"]:
            try:
                self.mm.remove_collision(self.mm.get_object("ExitDoor"))
            except ValueError:
                pass
            self.mm.remove_element_to_draw_obj(31, 34)
            self.mm.remove_element_to_draw_obj(31, 35)


    def supr_arbre(self):
        self.mm.maps[self.mm.current_map].group.remove(self.a)

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(
            self.default()) else self.default()
        if not self.actionb["Arbre"]:
            self.load_arbre()
        else:
            self.mm.remove_collision(self.mm.get_object("Arbrecollision"))
        self.opendoor()
        self.load_tile_map()
        self.allmap.load()

    def __str__(self):
        return "la map actuel est la foret"


    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if self.allmap.check_price(element) is False: break

                if "Arbre" in element[0].name and not self.actionb[element[0].name]:
                    self.supr_arbre()
                    self.actionb[element[0].name] = True
                    self.mm.remove_collision(self.mm.get_object("Arbrecollision"))
                if "Door" in element[0].name:
                    self.actionb["Door"] = False
                    self.opendoor()
                self.allmap.collision(element)

    def update(self):
        pass


class Maison_Foret:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Maison_Foret"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}
        self.allmap = Allmap(self.mm, self)

    def default(self):
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(
            self.default()) else self.default()
        self.allmap.load()

    def __str__(self):
        return "la map actuel est la Maison_Foret"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if self.allmap.check_price(element) is False: break
                self.allmap.collision(element)


    def update(self):
        pass


class Plaine:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Plaine"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        self.allmap = Allmap(self.mm, self)

    def default(self):
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None and len(
            self.mm.load(self.name)) == len(
            self.default()) else self.default()
        self.allmap.load()

    def __str__(self):
        return "la map actuel est Plaine"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if self.allmap.check_price(element) is False: break
                self.allmap.collision(element)

    def update(self):
        pass


class MaisonP??cheur:
    def __init__(self, mapmanager, save_load=False):
        self.name = "MaisonP??cheur"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        self.allmap = Allmap(self.mm, self)

    def load(self):
        self.allmap.load()

    def __str__(self):
        return "la map actuel est MaisonP??cheur"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if "p??cheur" in element[0].name:
                    objet2 = inv.item(26, 1)
                    self.mm.player.inventaire.add(objet2, "c14")
                #if "rubisBoss" in element[0].name:

                self.allmap.collision(element)


    def update(self):
        pass


class Plage:
    def __init__(self, mapmanager, save_load=False):
        self.name = "Plage"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        self.allmap = Allmap(self.mm, self)

    def default(self):
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None else self.default()
        self.allmap.load()

    def __str__(self):
        return "la map actuel est Plage"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if self.allmap.check_price(element) is False: break
                self.allmap.collision(element)

    def update(self):
        pass


class MaisonPlage:
    def __init__(self, mapmanager, save_load=False):
        self.name = "MaisonPlage"
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        self.allmap = Allmap(self.mm, self)

    def default(self):
        a = {}
        for i in self.mm.get_allobject("all"):
            try:
                a[i[0].name] = i[0].properties["default"]
            except KeyError:
                pass
        return a

    def load(self):
        self.actionb = self.mm.load(self.name) if self.mm.load(self.name) != None else self.default()
        self.allmap.load()

    def __str__(self):
        return "la map actuel est MaisonPlage"

    def collision(self, i):
        for element in self.mm.get_allobject("all"):
            if element[0].type != "InputAction":
                if i.feet.colliderect(element[1]):
                    self.allmap.collision_without_action(element)
                    break
                else:
                    self.mm.player.speed = self.mm.player.basespeed
            if i.feet.colliderect(
                    element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
                if self.allmap.hand(element) is False: break
                if self.allmap.check_price(element) is False: break
                self.allmap.collision(element)

    def update(self):
        pass


class Allmap():
    def __init__(self, mapmanager, map=None):
        self.mm = mapmanager
        self.map = map
        self.spawnpoint = None

        self.Ms_Spawn = PG.son("../song/Ingame/spawnpoint.mp3", "song")
        self.Ms_Spawn.volume(valeurs.valeur.volume)

        self.in_a_zone = False

        self.time_in = 0
        self.banc = False

    def load(self):
        if self.map.name == self.mm.current_map:
            if self.mm.current_map == self.mm.load_localtion():
                self.spawnpoint = self.mm.current_map
                self.mm.add_element_to_draw_obj("Base3", 201, self.mm.get_object("PlayerPos").x // 32,
                                                self.mm.get_object("PlayerPos").y // 32 - 1, 32)
                self.mm.add_element_to_draw_obj("Base3", 216, self.mm.get_object("PlayerPos").x // 32 - 1,
                                                self.mm.get_object("PlayerPos").y // 32, 32)
                self.mm.add_element_to_draw_obj("Base3", 218, self.mm.get_object("PlayerPos").x // 32 + 1,
                                                self.mm.get_object("PlayerPos").y // 32, 32)
                self.mm.add_element_to_draw_obj("Base3", 233, self.mm.get_object("PlayerPos").x // 32,
                                                self.mm.get_object("PlayerPos").y // 32 + 1, 32)
                self.Ms_Spawn.play()
            else:
                self.mm.remove_element_to_draw_obj(self.mm.get_object("PlayerPos").x // 32,
                                                   self.mm.get_object("PlayerPos").y // 32 - 1)
                self.mm.remove_element_to_draw_obj(self.mm.get_object("PlayerPos").x // 32 - 1,
                                                   self.mm.get_object("PlayerPos").y // 32)
                self.mm.remove_element_to_draw_obj(self.mm.get_object("PlayerPos").x // 32 + 1,
                                                   self.mm.get_object("PlayerPos").y // 32)
                self.mm.remove_element_to_draw_obj(self.mm.get_object("PlayerPos").x // 32,
                                                   self.mm.get_object("PlayerPos").y // 32 + 1)

    def hand(self, element):
        """
        Si l'??l??ment a une propri??t?? appel??e "needitem" et que le joueur a l'objet dans son inventaire, et que l'objet est
        le bon objet, et que le joueur a la bonne quantit?? de l'objet, alors l'objet est consomm??

        :param element: L'??l??ment avec lequel on interagit
        :return: une valeur bool??enne.
        """
        try:
            if element[0].properties["needitem"] != 0:  # On regarde si on a besoin de la propri??t?? needitem
                if self.mm.player.get_item_in_inventory(
                        5).obj is not None:  # On regarde que la main sois pas vide
                    if self.mm.player.get_item_in_inventory(5).obj.nom == element[0].properties[
                        "needitem"] and self.mm.player.get_item_in_inventory(5).obj.nbr >= \
                            element[0].properties[
                                "quantity"]:  # On regarde si c'est le bon objet et la bonne quantit??
                        if element[0].properties["consume"]:
                            if element[0].name in self.map.actionb.keys():
                                if not self.map.actionb[element[0].name]:
                                    self.mm.player.inventaire.suppr_nb_obj(element[0].properties["quantity"], 5)
                            else:
                                self.mm.player.inventaire.suppr_nb_obj(element[0].properties["quantity"], 5)
                    else:
                        self.action_help(element)
                        return False
                else:
                    self.action_help(element)
                    return False
        except (AttributeError, KeyError):
            pass

    def check_price(self, element):
        # V??rifier si le joueur a d??j?? achet?? l'article.
        if "Buy" in element[0].name:
            if not self.map.actionb[element[0].name]:  # On regarde si on a pas d??ja acheter l'item / Maison
                self.mm.player.gui.buy(element[0], self)
                return False
            return True

    def collision(self, element):
        try:
            a = element[0].properties['song']
            self.mm.song[a].play()
        except KeyError:
            pass
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
            try:
                var3 = element[0].properties['anim?']
            except KeyError:
                var3 = True
            if var3:
                self.mm.Animation.one_by_one_iblit(self.mm.screen, "fade_in")
            self.mm.save(self.mm.maps[self.mm.current_map].name)
            self.mm.player.allinputoff(False)
            self.mm.changemap(var, var2)

            if self.mm.current_map != var:
                self.load()

            self.mm.draw()

            if var3:
                self.mm.Animation.one_by_one_iblit(self.mm.screen, "fade_out")
            self.mm.player.allinputoff(True)

        if "Marchant" in element[0].name:
            self.mm.player.gui.shop(element[0].name)

        if "Banc" in element[0].name:
            if not self.banc:
                self.mm.player.moveinputoff(False)
                self.mm.player.rect.centerx, self.mm.player.rect.centery = element[0].x+element[0].width/2, element[0].y+element[0].height/2
                self.banc = True
                self.mm.player.animation(element[0].properties['Dirrection'])
            else:
                if element[0].properties["Dirrection"] == "down":
                    self.mm.player.rect.centery += 10
                elif element[0].properties["Dirrection"] == "up":
                    self.mm.player.rect.centery -= 10
                elif element[0].properties["Dirrection"] == "right":
                    self.mm.player.rect.centerx += 10
                elif element[0].properties["Dirrection"] == "left":
                    self.mm.player.rect.centerx -= 10
                self.banc = False
                self.mm.player.moveinputoff(True)

    def buy(self, element):
        """
        Si le joueur a assez d'argent, l'objet est achet?? et l'argent du joueur est r??duit du co??t de l'objet

        :param element: l'??l??ment que le joueur essaie d'acheter
        """
        if int(self.mm.player.money) >= int(element.properties['money']):
            self.map.actionb[element.name] = True
            self.mm.player.money -= int(element.properties['money'])
            self.save_player_info()
        else:
            print('pas assez dargent')

    def save_player_info(self):
        """
        Il enregistre les informations du joueur dans un fichier
        """
        w = open(valeurs.valeur.save_l + "/save/sauvegarde.txt", "w")
        w.write("SpawnPoint: " + str(self.map.name) + "\n")
        w.write("Money: " + str(self.mm.player.money) + "\n")
        w.write("Pseudo: " + str(self.mm.player.name) + "\n")

        print("Info enregistrer dans le fichier")
        w.close()

        self.mm.save(self.mm.maps[self.mm.current_map].name)

    def action_help(self, element):
        if "help" in element[0].name:
            self.mm.player.gui.Mind(element[0].properties['Texte'])

    def collision_without_action(self, element):
        a = element[0].name if isinstance(element[0].name, str) else ""
        b = element[0].type if isinstance(element[0].type, str) else ""
        if "Spike" in a:
            self.time_in += 1
            if self.time_in > 80:
                self.time_in = 0
                self.mm.player.hp -= element[0].properties['Damage']
                try:
                    a = element[0].properties['song']
                    self.mm.song[a].play()
                except KeyError:
                    pass
        if "SpawnPoint" in b:
            self.mm.player.hp = self.mm.player.hpmax
            if self.mm.current_map != self.spawnpoint:
                self.load()
                self.save_player_info()
        if "effect" in b:
            if "Boue" in b:
                self.mm.player.speed = int(element[0].properties["ralenti"])
