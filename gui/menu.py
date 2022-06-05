import datetime
import pickle

import pygame
import pygame_menu

from game_module.AI.easy_AI import Easy_AI
from game_module.AI.medium_AI import Medium_AI
from game_module.clock import Clock
from game_module.game import Game


class Menu:
    def __init__(self):
        self.handicap = 0
        self.size = 19
        self.game_mode = None
        self.hour = 0
        self.minute = 5
        self.second = 0
        self.type_game_mode = {
            "0": None,
            "1": Easy_AI(),
            "2": Medium_AI()
        }
        self.upgrade()

    def set_handicap(self, handicap):
        self.handicap = int(handicap)

    def set_size(self, value, size):
        self.size = size

    def set_game_mode(self, value, game_mode):
        self.game_mode = self.type_game_mode[str(game_mode)]

    def set_hour(self, value):
        self.hour = int(value)

    def set_minute(self, value):
        self.minute = int(value)

    def set_second(self, value):
        self.second = int(value)

    def start_the_game(self):
        g = Game(size=self.size,
                 handicap_point=self.handicap,
                 clock=Clock(datetime.time(self.hour, self.minute, self.second)), game_mode=self.game_mode)
        g.init_pygame()
        g.init_logic_prm()
        g.clear_screen()
        while True:
            g.update()
    def load_game(self):
        pass

    def upgrade(self):
        pygame.init()
        surface = pygame.display.set_mode((600, 400))
        menu = pygame_menu.Menu('Go', 600, 400,
                                theme=pygame_menu.themes.THEME_SOLARIZED)

        menu.add.text_input('Фора: ', default='0', onchange=self.set_handicap)
        menu.add.label("Время на ход:")
        menu.add.range_slider("Часы: ", default=0, range_values=(0, 24), increment=1, font_size=15,
                              onchange=self.set_hour)
        menu.add.range_slider("Минуты ", default=0, range_values=(0, 59), increment=1, font_size=15,
                              onchange=self.set_minute)
        menu.add.range_slider("Секунды ", default=1, range_values=(1, 59), increment=1, font_size=15,
                              onchange=self.set_second)
        menu.add.selector('Размер :', [('19x19', 19), ('13x13', 13), ('9x9', 9)], onchange=self.set_size)
        menu.add.selector('Режим игры', [('Hot seat', 0), ('Easy AI', 1), ('Medium AI', 2)],
                          onchange=self.set_game_mode)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(surface)


if __name__ == "__main__":
    Menu()
