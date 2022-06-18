import datetime

import pygame
import pygame_menu

from game_module.AI.easy_AI import EasyAI
from game_module.AI.medium_AI import MediumAI
from game_module.clock import Clock
from game_module.game import Game


class GameMenu:
    def __init__(self):
        # -------------------------------------------------------------------------
        # Create game menu
        # -------------------------------------------------------------------------
        pygame.init()
        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        self.menu = pygame_menu.Menu('Game', 600, 400,
                                     theme=pygame_menu.themes.THEME_SOLARIZED)
        self.handicap = self.menu.add.text_input(
            'Фора: ',
            default=0,
            maxchar=2,
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False)
        self.size = self.menu.add.selector('Размер :',
                                           [('19x19', 19), ('13x13', 13), ('9x9', 9)]
                                           )
        self.game_mode = self.menu.add.selector('Режим игры',
                                                [('Hot seat', None), ('Easy AI', EasyAI()),
                                                 ('Medium AI', MediumAI())],
                                                default=0,
                                                )
        self.menu.add.label("Время на ход:")
        self.hour = self.menu.add.range_slider("Часы: ",
                                               default=0,
                                               range_values=(0, 24),
                                               increment=1,
                                               font_size=15
                                               )
        self.minute = self.menu.add.range_slider("Минуты ",
                                                 default=5,
                                                 range_values=(0, 59),
                                                 increment=1,
                                                 font_size=15
                                                 )
        self.second = self.menu.add.range_slider("Секунды ",
                                                 default=1,
                                                 range_values=(1, 59),
                                                 increment=1,
                                                 font_size=15
                                                 )
        self.user_name: str = ""
        self.menu.add.button('Играть', self.start_the_game)

    def get_menu(self):
        return self.menu

    def start_the_game(self):
        g = Game(size=self.size.get_value()[0][1],
                 handicap_point=int(self.handicap.get_value()),
                 clock=Clock(datetime.time(int(self.hour.get_value()),
                                           int(self.minute.get_value()),
                                           int(self.second.get_value()))),
                 game_mode=self.game_mode.get_value()[0][1],
                 user_name=self.user_name)
        g.init_pygame()
        g.init_logic_prm()
        g.clear_screen()
        while True:
            g.update()
