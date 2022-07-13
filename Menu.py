from copy import copy

import pygame
from Button import *
from Player import Player
from Text import Text


class Menu:
    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load("img/menu/background.png")
        self.background_rect = pygame.Rect((0, 0), (855, 585))

        if "forte" in pygame.font.get_fonts():
            font = "forte"
        else:
            font = None
        print("Font:", font)
        self.font = pygame.font.SysFont(font, 40)
        self.font2 = pygame.font.SysFont(font, 25)
        self.key_listening = False
        self.key_cord = None

        # 0 - menu, 1 settings
        self.screen = 0

        self.menu_object = []
        self.settings_object = []
        self.add_menu_object()
        self.add_settings_object()
        self.draw()

    def add_menu_object(self):
        # start button
        img = pygame.image.load("img/menu/button_start.png")
        self.menu_object.append(
            Button(self.game, self, (427, 160), (84, 50), img,
                   self.game.start_lvl,
                   True
                   ))
        # settings button
        img = pygame.image.load("img/menu/button_settings.png")
        self.menu_object.append(
            Button(self.game, self, (427, 220), (153, 50), img,
                   self.go_to_settings,
                   True
                   ))

    def add_settings_object(self):
        # player name
        for i in range(4):
            img = self.font.render(f"Gracz {i + 1}", True,
                                   ((255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0))[i]
                                   )
            self.settings_object.append(
                Text(self.game, self,
                     (30, 150 + i * 80), (img.get_size()),
                     img
                     )
            )
        # column name
        for i in range(5):
            img = self.font.render(
                ("Lewo", "Góra", "Prawo", "Dół", "Bomba")[i],
                True,
                (0, 0, 0)
            )
            self.settings_object.append(
                Text(self.game, self,
                     (230 + 135 * i, 100), (img.get_size()),
                     img, True
                     )
            )
        # player key
        for i in range(4):
            for j in range(5):
                key = Player.key_player[i][j]
                img = self.font2.render(
                    self.key_to_str(key),
                    True,
                    (0, 0, 0)
                )
                self.settings_object.append(
                    Button1(self.game, self,
                            (230 + 135 * j, 175 + i * 80), (img.get_size()),
                            img,
                            self.change_player_button_click,
                            [i, j], True
                            )
                )
        # back button
        img = pygame.image.load("img/menu/button_settings.png")
        self.settings_object.append(
            Button(self.game, self, (300, 500), (153, 50), img,
                   self.go_to_menu,
                   True
                   ))


    def change_player_button_click(self, params):
        self.key_cord = params
        self.key_listening = True

    def change_player_button_button(self, key):
        if not any(key in pk for pk in Player.key_player):

            i,j=self.key_cord
            Player.key_player[i][j] = key
            img = self.font2.render(
                self.key_to_str(key),
                True,
                (0, 0, 0)
            )
            button = Button1(self.game, self,
                             (230 + 135 * j, 175 + i * 80), (img.get_size()),
                             img,
                             self.change_player_button_click,
                             [i, j], True
                             )

            self.settings_object[4 + 5 + i * 5 + j] = button
            self.key_listening = 0
            self.draw()

    def draw(self):
        self.game.display.blit(self.background, (0, 0))
        self.game.to_update.append(self.background_rect)
        if self.screen == 0:
            for o in self.menu_object:
                o.draw()
        elif self.screen == 1:
            for o in self.settings_object:
                o.draw()

    def next_frame(self, delta_time):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.key_listening = 0

                pos = pygame.mouse.get_pos()
                if self.screen == 0:
                    for o in self.menu_object:
                        o.click(pos)
                elif self.screen == 1:
                    for o in self.settings_object:
                        o.click(pos)

            if self.key_listening and event.type == pygame.KEYDOWN:
                print("Pressed")
                key = event.key
                self.change_player_button_button(key)

    def go_to_settings(self):
        self.screen = 1
        self.draw()

    def go_to_menu(self):
        self.screen = 0
        self.draw()


    @staticmethod
    def key_to_str(key):
        name = pygame.key.name(key)
        if len(name) == 3 and name[0] == "[" and name[2] == "]":
            name = f"NUM {name[1]}"
        return name.upper()
