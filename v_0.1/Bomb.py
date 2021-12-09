import pygame
from MovableObject import MovableObject
from Field import Field
from Fire import Fire


class Bomb(MovableObject):
    def __init__(self, game, position, player):
        # bomb, ready to explode, exploded, waiting, ending
        self.state = 0

        self.timer = 5000
        self.time_fire = 80
        self.time_time = 3000

        self.images = game.bomb_images
        self.owner = player
        self.fires: list[Fire] = []

        super().__init__(game, [game.size * position[0], game.size * position[1]], self.images[0], False)

        self.my_background[0].add_object(self)

        self.moving = True

        self.speed = 1
        self.power = 5

    def move_object(self):  # type: ()-> bool
        if self.state == 0:
            if super().move_object():
                self.kick(self.direction)
                return True
        elif self.state == 1:
            if self.movement == 0:
                self.explode()
            else:
                super().move_object()
        return False

    def can_kick(self):
        return self.state == 0

    def set_move_parameters(self, destination: tuple[int, int], next_background: Field):
        super().set_move_parameters(destination, next_background)
        next_background.add_object(self)

    def kick(self, direction):
        if self.state == 0 and self.movement == 0:
            self.direction = direction
            x = self.position[0]
            y = self.position[1]
            if self.direction == 0 and self.background[x - 1][y].can_entry_bomb():
                self.set_move_parameters((self.cords[0] - self.game.size, self.cords[1]), self.background[x - 1][y])
            elif self.direction == 1 and self.background[x][y - 1].can_entry_bomb():
                self.set_move_parameters((self.cords[0], self.cords[1] - self.game.size), self.background[x][y - 1])
            elif self.direction == 2 and self.background[x + 1][y].can_entry_bomb():
                self.set_move_parameters((self.cords[0] + self.game.size, self.cords[1]), self.background[x + 1][y])
            elif self.direction == 3 and self.background[x][y + 1].can_entry_bomb():
                self.set_move_parameters((self.cords[0], self.cords[1] + self.game.size), self.background[x][y + 1])
            else:
                return False
            return True

        elif self.state == 1:
            self.explode()
        return False

    def change_timer(self, dt):
        self.timer -= dt
        if self.timer < 0:
            if self.state == 0:
                self.state = 1
            elif self.state == 1:
                pass
            elif self.state == 2:
                self.power -= 1
                if self.power:
                    for f in self.fires:
                        f.next()
                    self.timer = self.time_fire
                else:
                    self.timer = self.time_time
                    self.state = 3

            elif self.state == 3:
                self.end()

    def explode(self):
        if self.state == 1:
            self.state = 2

            self.set_cords((self.position[0] * self.game.size, self.position[1] * self.game.size))
            self.owner.bomb_counter -= 1
            self.fires = [Fire(self.game, self, self.position, 4, 0),
                          Fire(self.game, self, self.position, 0, self.power),
                          Fire(self.game, self, self.position, 1, self.power),
                          Fire(self.game, self, self.position, 2, self.power),
                          Fire(self.game, self, self.position, 3, self.power),
                          ]

            self.timer = self.time_fire

    def draw(self):
        if self.state == 2 or self.state == 3:
            self.image = self.images[1][0]
            for f in self.fires:
                f.draw()
        elif self.state == 1:
            self.image = self.images[0][4]
        elif self.state == 0:
            if self.timer > 3500:
                self.image = self.images[0][0]
            elif self.timer > 2500:
                self.image = self.images[0][1]
            elif self.timer > 1500:
                self.image = self.images[0][2]
            elif self.timer > 100:
                self.image = self.images[0][3]
            elif self.timer > 0:
                self.image = self.images[0][4]

        super().draw()

    def can_entry(self):
        return self.state >= 2

    def hide(self):
        for f in self.fires: f.hide()
        super().hide()

    def end(self):
        for f in self.fires: f.delete()
        super().hide()
        for b in self.my_background:
            b.remove_object(self)
        self.game.bomb_list.remove(self)

        self.fires = []

    def end_move(self):
        self.my_background[0].remove_object(self)
        super().end_move()

    def destroy(self):
        if self.state < 2:
            self.state = 1
            self.set_cords((self.position[0] * self.game.size, self.position[1] * self.game.size))
            self.explode()
        else:
            return False
