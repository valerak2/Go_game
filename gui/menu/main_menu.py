import pygame
import pygame_menu

from gui.menu.game_menu import GameMenu
from gui.menu.table_menu import TableMenu


class MainMenu:
    def __init__(self):
        self.main_menu = None
        self.game_menu = GameMenu()
        self.table_records = TableMenu()

    def load_game(self):
        pass

    def set_user_name(self, text: str):
        if text == "":
            text = "Гость"
        field_user_name = self.main_menu.add.label(
            'Пользователь: ' + text,
            float=True,
            font_name=pygame_menu.font.FONT_OPEN_SANS_ITALIC,
            font_size=25)
        field_user_name.translate(200, -200)

    def create_menu(self):
        # -------------------------------------------------------------------------
        # Create menus: Main
        # -------------------------------------------------------------------------
        pygame.init()
        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

        self.main_menu = pygame_menu.Menu('Go', 600, 400,
                                          theme=main_theme,
                                          )

        self.main_menu.add.button('Играть', self.game_menu.get_menu())
        self.main_menu.add.button('Таблица рекордов', self.table_records.get_menu())
        self.main_menu.add.button('Выход', pygame_menu.events.EXIT)

    def upgrade(self):

        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)

        def on_resize() -> None:
            window_size = surface.get_size()
            new_w, new_h = window_size[0], window_size[1]
            self.main_menu.resize(new_w, new_h)
            self.game_menu.get_menu().resize(new_w, new_h)
            self.table_records.get_menu().resize(new_w, new_h)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.VIDEORESIZE:
                    surface = pygame.display.set_mode((event.w, event.h),
                                                      pygame.RESIZABLE)
                    on_resize()
                if event.type == pygame.QUIT:
                    exit()

            self.main_menu.update(events)
            if self.main_menu.is_enabled():
                self.main_menu.draw(surface)
            pygame.display.flip()
