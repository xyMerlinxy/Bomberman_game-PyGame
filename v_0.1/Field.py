import pygame
from Object import Object


class Field(Object):
    def __init__(self, game, name, cords, image):
        self.name = name
        super().__init__(game, cords, image, self.name == 0)

        self.object = []
        self.number_of_player = 0

    def can_entry(self):
        # print(f"Move to: {self} number of object: {len(self.object)}")
        return self.possibility_of_entry and sum(obj.can_entry() for obj in self.object) == len(self.object)

    def can_entry_bomb(self): return self.can_entry() and self.number_of_player == 0

    def can_kick(self):
        return 0 < len(self.object) == sum(obj.can_kick() for obj in self.object)

    def kick(self, direction):
        for o in self.object:
            if o.kick(direction): return True
        return False

    def __str__(self):
        return f"Cords: {self.cords} Name: {self.name} Entry: {self.possibility_of_entry}"

    def add_object(self, obj: Object):
        self.object.append(obj)
        # print(f"Added object to {self} Object: {len(self.object)}")

    def remove_object(self, obj: Object):
        # print(f"Remove object to {self} Object: {len(self.object)}")
        if obj in self.object: self.object.remove(obj)

    def destroy(self):
        #print(self.object, sum(1 for o in self.object if o.destroy))
        return sum(1 for o in self.object if o.destroy())>0