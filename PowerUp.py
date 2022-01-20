import random

import pygame

import Player
from Object import Object


class PowerUp(Object):
    number_of_powerups = 5

    def __init__(self, game, position: list[int, int]):
        # id [bomb +1, bomb -1, insensitivity]
        # TODO balance drop rate
        self.id = random.randint(0, 4)
        #self.id=random.randint(3,4)
        super().__init__(game,
                         [game.size * position[0], game.size * position[1]],
                         game.powerUp_images[self.id],
                         True, (5, 5),
                         (game.size - 10, game.size - 10)
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
            player.bomb_max += 1
            # TODO move check player max_bomb to setter
        elif self.id == 1 and player.bomb_max > 1:
            player.bomb_max -= 1
        elif self.id == 2:
            player.insensitivity_on()
        elif self.id == 3:
            player.speed *= 1.5
            print("Speed:",player.speed)
            # TODO move check player max_bomb to setter
        elif self.id == 4 and player.speed > 1.5:
            player.speed = player.speed/150*100
            if player.speed < 1.5:player.speed=1.5
            print("Speed:",player.speed)
