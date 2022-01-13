from Field import Field
from Object import Object

FIRE_TYPE_CENTER = 0
FIRE_TYPE_HORIZONTAL = 1
FIRE_TYPE_VERTICAL = 2


class FireSegment(Object):
    def __init__(self, game, cords, image, possibility_of_entry, fire_type):
        rect_offset = (10 if fire_type == 2 else 0, 10 if fire_type == 1 else 0)
        rect_size = (game.size - (20 if fire_type == 2 else 0), game.size - (20 if fire_type == 1 else 0))
        super().__init__(game, cords, image, possibility_of_entry, rect_offset, rect_size)


class Fire:
    def __init__(self, game, bomb, begin_position: list[int, int], direction: int = 0, power: int = 0):
        self.owner = bomb
        self.game = game
        self.begin_position: list[int, int] = list(begin_position)

        self.my_background: list[Field] = []

        self.type = FIRE_TYPE_CENTER if direction == 4 else (
            FIRE_TYPE_VERTICAL if direction == 0 or direction == 2 else FIRE_TYPE_HORIZONTAL)

        # center of fire
        if direction == 4:
            pos = begin_position
            img = self.game.bomb_images[1][0]
            field = self.game.get_background(pos)
            self.my_background.append(field)
            self.fire_segments = [
                FireSegment(self.game, [self.game.size * pos[0], self.game.size * pos[1]], img, True, self.type)]
            self.my_background.append(field)
            field.add_object(self.fire_segments[0])
            # destroy object under fire
            for i in self.my_background[0].object:
                i.destroy()
        else:
            self.images = [self.game.bomb_images[1][1][direction],
                           self.game.bomb_images[1][2][direction]]
            self.fire_segments: list[FireSegment] = []

        self.direction = direction
        self.power = power

        self.type = [1, 2][direction % 2] if direction != 4 else 0

        self.next()

    def next(self):
        if self.power > 0:
            self.power -= 1
            if self.direction == 0:
                self.begin_position[0] -= 1
            elif self.direction == 1:
                self.begin_position[1] -= 1
            elif self.direction == 2:
                self.begin_position[0] += 1
            elif self.direction == 3:
                self.begin_position[1] += 1

            pos = self.begin_position
            if len(self.fire_segments): self.fire_segments[-1].set_image(self.images[0])

            field = self.game.get_background(pos)
            if field.destroy(): self.power = 0

            if field.can_entry():
                fire_segment = FireSegment(self.game, [self.game.size * pos[0], self.game.size * pos[1]],
                                           self.images[1],
                                           True, self.type)
                self.fire_segments.append(fire_segment)
                self.my_background.append(field)
                field.add_object(fire_segment)
            else:
                self.power = 0

    def draw(self):
        for f in self.fire_segments: f.draw()

    def hide(self):
        for f in self.my_background: f.draw()

    def delete(self):
        self.hide()
        for fire, field in zip(self.fire_segments, self.my_background):
            field.remove_object(fire)

        self.fire_segments = []
        self.my_background = []
        self.owner = None
