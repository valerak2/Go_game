from game_module.AI.ai import AI


class MediumAI(AI):
    def __init__(self):
        self.player_move_col = 3
        self.player_move_row = 4

    def record__player_move(self, col, row):
        self.player_move_col = col
        self.player_move_row = row

    def move(self):
        point = [18 - self.player_move_col, self.player_move_row]
        return point
