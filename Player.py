import pygame
from MovableObject import MovableObject
from Bomb import Bomb
from Field import Field


# TODO somethings wrong when press 4 keys for one player (probably hardware)


class Player(MovableObject):
    key_player = [
        [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RCTRL],
        [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_SPACE]
    ]

    def __init__(self, game, cords, number):
        self.id = number
        self.images = self.load_images()

        super().__init__(game, cords, self.images[0], True, (9, 1), (25, 43))
        self.my_background[0].number_of_player += 1

        self.speed = 2.9
        self.key = Player.key_player[self.id]

        print(self.id)
        print(self.position, self.x, self.y, self.cords)

        self.bomb_counter = 0
        self.bomb_max = 3

        self.pressed_key = []

        self.lives = 1
        self.insensitivity = False

    def load_images(self):
        return [pygame.image.load(f"img\\player\\player_{self.id}_stay.png"),
                pygame.image.load(f"img\\player\\player_{self.id}_go.png")]

    def draw(self):
        if 10 < self.distance_to_move < 35:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        super().draw()

    def press_key(self, key):
        if key in self.key:
            if self.key.index(key) == 4:
                self.plant_bomb()
            else:
                if key in self.pressed_key: self.pressed_key.remove(key)
                self.pressed_key.append(key)

    def plant_bomb(self):
        if self.bomb_max > self.bomb_counter and self.background[self.position[0]][self.position[1]].can_entry():
            self.game.bomb_list.append(Bomb(self.game, self.position, self))
            self.bomb_counter += 1
            print(
                f"Bomb placed: {self.position}, {self.bomb_max}>{self.bomb_counter} ID:{self.id}, {self.game.bomb_list[-1]}")

    def release_key(self, key):
        if key in self.key and self.key.index(key) < 4:
            self.pressed_key.remove(key)

    def set_move_parameters(self, destination, next_background: Field, direction=0):
        self.direction = direction
        super().set_move_parameters(destination, next_background)

        self.my_background[-1].number_of_player += 1
        # print()
        # print(f"{self.my_background[0].cords} Num of player: {self.my_background[0].number_of_player}")
        # print(f"{self.my_background[1].cords} Num of player: {self.my_background[1].number_of_player}")

    def start_move(self):

        if self.movement == 0 and len(self.pressed_key):
            for k in self.pressed_key[::-1]:
                self.direction = self.key.index(k)
                if self.reaction_for_key(k):
                    break

    def reaction_for_key(self, key):
        x = self.position[0]
        y = self.position[1]
        if key == self.key[0] and (self.background[x - 1][y].can_entry() or self.background[x - 1][y].can_kick()):
            if self.background[x - 1][y].can_entry():
                self.set_move_parameters((self.cords[0] - self.game.size, self.cords[1]), self.background[x - 1][y], 0)
                return True
            elif self.background[x - 1][y].kick(0):
                return True
        elif key == self.key[1] and (self.background[x][y - 1].can_entry() or self.background[x][y - 1].can_kick()):
            if self.background[x][y - 1].can_entry():
                self.set_move_parameters((self.cords[0], self.cords[1] - self.game.size), self.background[x][y - 1], 1)
                return True
            elif self.background[x][y - 1].kick(1):
                return True
        elif key == self.key[2] and (self.background[x + 1][y].can_entry() or self.background[x + 1][y].can_kick()):
            if self.background[x + 1][y].can_entry():
                self.set_move_parameters((self.cords[0] + self.game.size, self.cords[1]), self.background[x + 1][y], 2)
                return True
            elif self.background[x + 1][y].kick(2):
                return True
        elif key == self.key[3] and (self.background[x][y + 1].can_entry() or self.background[x][y + 1].can_kick()):
            if self.background[x][y + 1].can_entry():
                self.set_move_parameters((self.cords[0], self.cords[1] + self.game.size), self.background[x][y + 1], 3)
                return True
            elif self.background[x][y + 1].kick(3):
                return True
        return False

    def end_move(self):
        self.my_background[0].number_of_player -= 1
        # print(f"{self.my_background[0].cords} Num of player: {self.my_background[0].number_of_player}")
        # print(f"{self.my_background[1].cords} Num of player: {self.my_background[1].number_of_player}")
        super().end_move()

    def destroy(self):
        if not self.insensitivity:
            self.lives -= 1
            if self.lives == 0:
                self.game.remove_player(self)
                self.hide()
        return False

    def set_insensitivity(self, insensitivity):
        print(f"Player {self.id} insensitivty {insensitivity}")
        self.insensitivity = insensitivity

    def collect(self, powerup):
        powerup.collect(self)
