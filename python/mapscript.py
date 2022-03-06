import pygame


class Grotte:
    def __init__(self, mapmanager, save_load=True):
        self.mm = mapmanager

        if save_load:
            self.actionb = self.mm.load()
        else:
            self.actionb = {"Pont": 0}
    
    def load(self):
        pass


    def collision(self,i):
        for element in self.mm.get_objectinp("InputAction", "all"):
                    if i.feet.colliderect(
                            element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
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
                        if "Panneau" in element[0].name:
                            self.mm.player.gui.DialogP(element[0].properties['Speaker'], element[0].properties['Texte'])
                        if "Torch" in element[0].name:
                            if element[0].name not in self.actionb.keys():
                                
                                self.actionb[element[0].name] = False
                            if not element[0].properties['Infire'] and not self.actionb[element[0].name]:
                                element[0].properties['Infire'] = True
                                self.actionb[element[0].name] = True
                                print(self.mm.get_layer_by_name(element[0].name+"0").visible)
                                self.mm.set_layer_visible(element[0].name+"0", True)
                                self.mm.actionnb['Pont'] += 1
                                self.mm.reloadmap()
                        if "Chest" in element[0].name:
                            self.mm.player.gui.inventory_chest(element[0].name, self.mm.player.inventaire)

                        else:
                            pass

    def update(self):
        if self.mm.get_object("Pont").properties['Enable']:
            if self.mm.actionnb['Pont'] == 5:
                self.mm.get_object("Pont").properties['Enable'] = False

            if not self.mm.get_object("Pont").properties['Enable']:
                self.mm.remove_collision(self.mm.get_object("Pont"))
                self.mm.set_layer_visible('Pont', True)

class lobby:
    def __init__(self, mapmanager, save_load = False):
        self.mm = mapmanager
        self.actionb = {}
        self.liste_obj = {}

        if save_load:
            pass
        else:
            pass
    
    def collision(self, i):
        for element in self.mm.get_objectinp("InputAction", "all"):
                    if i.feet.colliderect(
                            element[1]) and self.mm.player.inputaction():  # si le joueurs entre en collision avec un objet
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

    def update(self):
        pass
