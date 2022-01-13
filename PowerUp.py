import random

import pygame

import Player
from Object import Object


class PowerUp(Object):

    def __init__(self, game, position: list[int, int]):
        # TODO draw porwerup id and type of powerup(red, yelow, green)
        self.id = 0
        self.type = random.randint(0, 1)
        super().__init__(game,
                         [game.size * position[0], game.size * position[1]],
                         game.powerUp_images[self.id][self.type],
                         True, (5, 5),
                         (game.size-10, game.size-10)
                         )
        self.game.powerUp_list.append(self)
        self.background = self.game.get_background(position)
        self.background.add_object(self)
        print(self.background.object)

    def destroy(self):
        self.background.remove_object(self)
        self.game.powerUp_list.remove(self)
        self.background.draw()
        return True

    def collect(self, player: Player):
        self.background.remove_object(self)
        self.game.powerUp_list.remove(self)
        self.background.draw()

        if self.id == 0:
            if self.type == 0: player.bomb_max += 1
            # TODO move check player max_bomb to setter
            if self.type == 1 and player.bomb_max > 1: player.bomb_max -= 1
