import pygame
from Object import Object
from PowerUp import PowerUp


class Wall(Object):

    def __init__(self, game, position: list[int, int],
                 image: pygame.Surface):
        super().__init__(game, [game.size * position[0], game.size * position[1]], image)
        self.background = self.game.get_background(position)
        self.background.add_object(self)
        self.pos = position

    def destroy(self):
        self.background.remove_object(self)
        self.game.walls_list.remove(self)
        self.background.draw()

        PowerUp(self.game,self.pos)

        return True


