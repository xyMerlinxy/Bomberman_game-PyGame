import pygame
from Field import Field
from Player import Player
from Bomb import Bomb
from Events import *
from PowerUp import PowerUp
from Wall import Wall


# TODO can_entry(self, who) check possibility of entry depend of the who ask
# TODO ?? Remove from fields object[] and add (wall, power_up,bomb)(solved ??)
# TODO add powerups
# PROPOSITION - add destroy wall animation

class Game:

    def __init__(self):
        self.size = 45
        self.fields_size = (19, 13)
        self.display_size = (self.fields_size[0] * self.size, self.fields_size[1] * self.size)

        pygame.init()
        pygame.display.set_caption("Bombowy człowiek")
        self.display = pygame.display.set_mode(self.display_size)

        self.to_update = []

        self.lvl_name = "lvl_1"
        self.background = []
        self.walls_list = []
        self.load_map(self.lvl_name)

        self.bomb_images = []
        self.load_bomb_images()
        self.bomb_list: list[Bomb] = []

        self.powerUp_images = []
        self.load_powerUp_images()
        self.powerUp_list: list[PowerUp]=[]

        self.all_players: list[Player] = [Player(self, [1 * self.size, 1 * self.size], 0),
                                          Player(self, [17 * self.size, 1 * self.size], 1)]
        self.alive_players: list[Player] = list(p for p in self.all_players)
        self.dead_players: list[Player] = []

        # self.alive_players[0].set_insensitivity(True)
        # self.alive_players[1].set_insensitivity(True)
        #
        # rise_event(PLAYER_0_INSENSITIVITY_OFF, 11000)
        # rise_event(PLAYER_1_INSENSITIVITY_OFF, 15000)

        # frames per second setting
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()
        self.delta_time = 0

        pygame.display.update()

    def load_map(self, lvl_name):
        self.background = []

        for i in range(self.fields_size[0]):
            self.background.append([])
            for j in range(self.fields_size[1]):
                self.background[i].append(0)

        # TODO make validation opened file
        file_map = open(f"map/{lvl_name}", "r")
        graphic_type = file_map.readline()[:-1]
        numbers_of_images = int(file_map.readline()[:-1])
        number_of_map_lines = int(file_map.readline()[:-1])

        loaded_images = []
        for i in range(numbers_of_images):
            print(f'map/{graphic_type}/{i}')
            loaded_images.append(pygame.image.load(f'map/{graphic_type}/{i}.bmp'))

        # TODO check if there is that folder
        for i in range(number_of_map_lines):
            line = file_map.readline()
            for j, field in enumerate(line.split()):
                self.background[j][i] = Field(self, int(field), [self.size * j, self.size * i],
                                              loaded_images[int(field)])

        wall_image = pygame.image.load(f'map/{graphic_type}/w0.bmp')
        # load wall cords
        walls_cord = file_map.readline().split(";")
        for cords in walls_cord:
            self.walls_list.append(Wall(self, list(map(int,cords.split(","))), wall_image))

    def load_bomb_images(self):
        # TODO make rotate image
        self.bomb_images = [
            [pygame.image.load("img/bomb/bomb_0.png"),
             pygame.image.load("img/bomb/bomb_1.png"),
             pygame.image.load("img/bomb/bomb_2.png"),
             pygame.image.load("img/bomb/bomb_3.png"),
             pygame.image.load("img/bomb/bomb_4.png"),
             ],
            [pygame.image.load("img/bomb/explosion_0.png"),
             [pygame.image.load("img/bomb/explosion_10.png"),
              pygame.image.load("img/bomb/explosion_11.png"),
              pygame.image.load("img/bomb/explosion_12.png"),
              pygame.image.load("img/bomb/explosion_13.png")],
             [pygame.image.load("img/bomb/explosion_20.png"),
              pygame.image.load("img/bomb/explosion_21.png"),
              pygame.image.load("img/bomb/explosion_22.png"),
              pygame.image.load("img/bomb/explosion_23.png")]
             ]
        ]

    def load_powerUp_images(self):
        number_of_powerups = 1
        F = pygame.image.load
        for i in range(number_of_powerups):
            self.powerUp_images.append(list(
                    F(f"img/powerup/p{i}_{j}.png")
                    for j in range(2)
                ))
        print(self.powerUp_images)

    def remove_player(self, player):
        self.alive_players.remove(player)
        self.dead_players.append(player)

    def start_game(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    for p in self.alive_players:
                        p.press_key(event.key)
                elif event.type == pygame.KEYUP:
                    for p in self.alive_players:
                        p.release_key(event.key)
                elif PLAYER_0_INSENSITIVITY_OFF <= event.type <= PLAYER_3_INSENSITIVITY_OFF:
                    if event.type == PLAYER_0_INSENSITIVITY_OFF:
                        self.all_players[0].set_insensitivity(False)
                    elif event.type == PLAYER_1_INSENSITIVITY_OFF:
                        self.all_players[1].set_insensitivity(False)
                    elif event.type == PLAYER_2_INSENSITIVITY_OFF:
                        self.all_players[2].set_insensitivity(False)
                    elif event.type == PLAYER_3_INSENSITIVITY_OFF:
                        self.all_players[3].set_insensitivity(False)
                    rise_event(event.type, 0)
            # keys = pygame.key.get_pressed()

            for p in self.alive_players: p.start_move()
            for p in self.alive_players: p.hide()
            for b in self.bomb_list: b.hide()

            for p in self.alive_players: p.move_object()
            for b in self.bomb_list: b.move_object()

            for b in self.bomb_list: b.change_timer(self.delta_time)

            #for w in self.walls_list: w.draw()
            for u in self.powerUp_list: u.draw()
            for b in self.bomb_list: b.draw()
            for p in self.alive_players: p.draw()

            pygame.display.update(self.to_update)
            self.to_update = []

            self.delta_time = self.fpsClock.tick_busy_loop(self.FPS)
            # self.fpsClock.tick(self.FPS)
            # pygame.time.wait(100)

    def get_background(self, position):  # type: (tuple[int, int])-> Field
        return self.background[position[0]][position[1]]


if __name__ == "__main__":
    new_game = Game()
    new_game.start_game()
