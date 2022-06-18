import pygame
import pygame_menu

from game_module.logger import get_table_record


class TableMenu:
    def __init__(self):
        # -------------------------------------------------------------------------
        # Create menus:Table records
        # -------------------------------------------------------------------------
        pygame.init()
        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.widget_margin = (0, 0)

        self.menu = pygame_menu.Menu('Table records', 600, 400,
                                     theme=theme,
                                     )
        self.fill_table()

    def fill_table(self):
        table_contrib = self.menu.add.table()
        table_contrib.default_cell_padding = 5
        table_contrib.default_row_background_color = 'white'
        bold_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
        table_contrib.add_row(
            ['Игрок', 'Побед в Hot seat', 'Побед против Easy AI', 'Побед против Medium AI', 'Всего побед'],
            cell_font=bold_font)
        table_record = get_table_record()
        for i in table_record:
            table_contrib.add_row(i)

        table_contrib.update_cell_style(-1, -1, font_size=15)  # Update all column/row
        table_contrib.update_cell_style(1, [2, -1], font=pygame_menu.font.FONT_OPEN_SANS_ITALIC)

    def get_menu(self):
        return self.menu
