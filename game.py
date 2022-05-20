from operations import *


class Game:
    def __init__(self, size):
        self.board = np.zeros((size, size))
        self.size = size
        self.black_turn = True
        self.prisoners = collections.defaultdict(int)
        self.start_points, self.end_points = make_grid(self.size)

    def init_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        self.screen = screen
        self.ZOINK = pygame.mixer.Sound("padenie-ogromnogo-predmeta-i-raskol-vdrebezgi.wav")
        self.CLICK = pygame.mixer.Sound("zvuk4.wav")
        self.font = pygame.font.SysFont("arial", 30)

    def clear_screen(self):

        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = col_row_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)

        pygame.display.flip()

    def pass_move(self):
        self.black_turn = not self.black_turn
        self.draw()

    def click(self):
        x, y = pygame.mouse.get_pos()
        col, row = xy_to_col_row(x, y, self.size)
        if not is_valid_move(col, row, self.board):
            self.ZOINK.play()
            return

        self.board[col, row] = 1 if self.black_turn else 2

        self_color = "black" if self.black_turn else "white"
        other_color = "white" if self.black_turn else "black"

        capture_happened = False
        for group in list(get_stone_groups(self.board, other_color)):
            if has_no_liberties(self.board, group):
                capture_happened = True
                for i, j in group:
                    self.board[i, j] = 0
                self.prisoners[self_color] += len(group)

        if not capture_happened:
            group = None
            for group in get_stone_groups(self.board, self_color):
                if (col, row) in group:
                    break
            if has_no_liberties(self.board, group):
                self.ZOINK.play()
                self.board[col, row] = 0
                return

        self.CLICK.play()
        self.black_turn = not self.black_turn
        self.draw()

    def draw(self):

        self.clear_screen()
        for col, row in zip(*np.where(self.board == 1)):
            x, y = col_row_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = col_row_to_xy(col, row, self.size)
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

        pygame.display.flip()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.click()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.pass_move()

if __name__ == "__main__":
    g = Game(size=19)
    g.init_pygame()
    g.clear_screen()

    while True:
        g.update()