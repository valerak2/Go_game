from typing import TextIO

import pygame
import pygame_menu
from pygame_menu.widgets import TextInput

from gui.get_file_name import table_record_path
from gui.menu.main_menu import MainMenu


class Authentication:
    def __init__(self):
        self.label = None
        self.authentication_menu = None
        self.main_menu: MainMenu
        self.USER_NAME = None
        self.USER_NAME: TextInput
        self.users = None
        self.correct_user_name = True
        self.getting_list_users()

    def write_new_user(self):
        file: TextIO = open(table_record_path(), "r", encoding='UTF-8')
        txt = file.read()
        file.close()

        file: TextIO = open(table_record_path(), "w", encoding='UTF-8')
        file.truncate(0)
        file.write(txt + "\n")
        file.write(self.USER_NAME.get_value() + " 0 0 0")
        file.close()

    def getting_list_users(self):
        file: TextIO = open(table_record_path(), "r", encoding='UTF-8')
        users = []
        for i in file.readlines():
            split = i.replace('\n', '').split(" ")
            if split.__len__() < 4:
                continue
            name = split[0]
            users.append(name)
        file.close()
        self.users = users

    def correct_name(self, name):
        return True if name in self.users else False

    def correct_new_name(self, name):
        return True if name not in self.users else False

    def check_correct_user(self):
        if self.correct_name(self.USER_NAME.get_value()):
            self.successful_authentication()
        else:
            self.change_label('Пользователя с таким именем нет')

    def check_correct_new_user(self):
        if self.correct_new_name(self.USER_NAME.get_value()):
            if self.USER_NAME.get_value() != "":
                self.write_new_user()
            self.successful_authentication()
        else:
            self.change_label('Имя уже занято')

    def successful_authentication(self):
        self.main_menu.create_menu()
        self.main_menu.set_user_name(self.USER_NAME.get_value())
        self.main_menu.game_menu.user_name = self.USER_NAME.get_value()
        self.main_menu.upgrade()

    def change_label(self, txt):
        self.label.set_title(txt)

    def create_menu(self):

        pygame.init()
        self.main_menu = MainMenu()
        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.authentication_menu = pygame_menu.Menu('Welcome', 600, 400,
                                                    theme=main_theme,
                                                    )
        self.USER_NAME = self.authentication_menu.add.text_input('Введите имя:', default='')

        self.label = self.authentication_menu.add.label('', font_size=15, font_color=(255, 0, 0))
        self.authentication_menu.add.button('Войти',
                                            self.check_correct_user,
                                            ).background_inflate_to_selection_effect()
        self.authentication_menu.add.button('Зарегистрироваться',
                                            self.check_correct_new_user,
                                            ).background_inflate_to_selection_effect()
        self.authentication_menu.add.label('Если вы хотите войти как гость,\n '
                                           'то оставьте поле имени пустым \n '
                                           'и нажмите кнопку регистрация', font_size=10)

        self.authentication_menu.add.button('Выход', pygame_menu.events.EXIT)

    def upgrade(self):
        def on_resize() -> None:
            window_size = surface.get_size()
            new_w, new_h = window_size[0], window_size[1]
            self.authentication_menu.resize(new_w, new_h)

        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.VIDEORESIZE:
                    surface = pygame.display.set_mode((event.w, event.h),
                                                      pygame.RESIZABLE)
                    on_resize()
                if event.type == pygame.QUIT:
                    exit()
            self.authentication_menu.update(events)
            if self.authentication_menu.is_enabled():
                self.authentication_menu.draw(surface)
            pygame.display.flip()
