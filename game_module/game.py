import collections
import itertools
import json
import sys

import pygame
import numpy as np
from pygame import gfxdraw
from game_module import game_constants
from game_module import AI
from game_module.AI.medium_AI import Medium_AI
from game_module.clock import Clock
from game_module.game_constants import BOARD_WIDTH, DOT_RADIUS, BLACK, BOARD_BROWN, STONE_RADIUS, WHITE, SCORE_POS, \
    TURN_POS, TIMER_POS, RES_POS

from game_module import logic_operations
from game_module.logger import Logger


class Game:
    def __init__(self, size, handicap_point: int, clock: Clock, game_mode: AI):
        self.size = size
        self.init_game_module(game_mode)
        self.board = np.zeros((size, size))
        self.clock: Clock = clock
        self.handicap_point = handicap_point

    def init_logic_prm(self):
        self.logger = Logger()
        self.black_turn = True
        self.game_on = True
        self.prisoners = collections.defaultdict(int)
        self.start_points, self.end_points = logic_operations.make_grid(self.size)

    def init_pygame(self):
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH), pygame.RESIZABLE)
        self.no_click_sound = pygame.mixer.Sound(game_constants.no_click)
        self.click_sound = pygame.mixer.Sound(game_constants.click)
        self.font = pygame.font.SysFont("arial", 30)

    def init_game_module(self, game_mode: AI):
        if game_mode is None:
            self.game_mode: game_mode = None
        else:
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
            self.game_mode: game_mode = game_mode

    def clear_screen(self):

        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = logic_operations.col_row_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)

        pygame.display.flip()

    def pass_move(self):
        self.black_turn = not self.black_turn
        self.draw()

    def click(self, x, y):
        col, row = logic_operations.xy_to_col_row(x, y, self.size)

        if not logic_operations.is_valid_move(col, row, self.board):
            self.no_click_sound.play()
            return
        self.clock.refresh()
        self.board[col, row] = 1 if self.black_turn else 2

        # отправка ИИ ход игрока
        if self.game_mode.__class__ == Medium_AI:
            self.game_mode.record__player_move(col, row)

        self_color = "black" if self.black_turn else "white"
        other_color = "white" if self.black_turn else "black"

        capture_happened = False
        for group in list(logic_operations.get_stone_groups(self.board, other_color)):
            if logic_operations.has_no_liberties(self.board, group):
                capture_happened = True
                for i, j in group:
                    self.board[i, j] = 0
                self.prisoners[self_color] += len(group)

        if not capture_happened:
            group = None
            for group in logic_operations.get_stone_groups(self.board, self_color):
                if (col, row) in group:
                    break
            if logic_operations.has_no_liberties(self.board, group):
                self.no_click_sound.play()
                self.board[col, row] = 0
                return

        self.click_sound.play()
        txt = (f"{'Черные' if self.black_turn else 'Белые'}"
               + " ход на:" + f"{col, row}")
        self.logger.write(txt)
        self.black_turn = not self.black_turn

        self.draw()

        # фора
        self.handicap_in_start_game()

    def handicap_in_start_game(self):
        if self.handicap_point > 0:
            self.handicap_point -= 1
            self.pass_move()

    def draw(self):

        self.clear_screen()
        for col, row in zip(*np.where(self.board == 1)):
            x, y = logic_operations.col_row_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = logic_operations.col_row_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, WHITE)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, WHITE)
        score_msg = (
                f"Пленных у черных: {self.prisoners['black']}"
                + f"     Пленных у белых: {self.prisoners['white']}"
        )
        txt = self.font.render(score_msg, True, BLACK)
        self.screen.blit(txt, SCORE_POS)
        turn_msg = (
                f"{'Черные' if self.black_turn else 'Белые'} ходят. "
                + "Нажмите P для пропуска хода."
        )
        txt = self.font.render(turn_msg, True, BLACK)
        self.screen.blit(txt, TURN_POS)

        txt = self.font.render(self.clock.in_txt(), True, BLACK)
        self.screen.blit(txt, TIMER_POS)
        if not self.game_on:
            turn_msg = f"{'Черные' if self.black_turn else 'Белые'} проиграли по времени. "
            txt = self.font.render(turn_msg, True, BLACK)
            self.screen.blit(txt, RES_POS)
        pygame.display.flip()

    def game_over(self):
        self.game_on = False
        self.draw()
        self.logger.record_in_table(self.black_turn, self.game_mode)
        self.logger.close()

    def update(self):
        if self.game_on:
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.black_turn:
                        x, y = pygame.mouse.get_pos()
                        self.click(x, y)
                    elif self.game_mode is None:
                        x, y = pygame.mouse.get_pos()
                        self.click(x, y)

                if event.type == pygame.USEREVENT:
                    self.clock.processing()
                    if self.clock.is_time_over():
                        self.game_over()
                    self.draw()

                if event.type == pygame.USEREVENT + 1:
                    if not self.black_turn and self.game_mode is not None:
                        point = self.game_mode.move()
                        x, y = logic_operations.col_row_to_xy(point[0], point[1], self.size)
                        self.click(x, y)

                if event.type == pygame.QUIT:
                    self.board.tolist()
                    print(self.board.tolist().__class__)
                    with open('save_game.json', 'w', encoding='utf-8') as f:
                        json.dumps(self.__dict__, ensure_ascii=False, indent=4)
                    sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        self.pass_move()
        else:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
