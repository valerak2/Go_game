from game_module.AI.ai import AI
from random import randrange


class EasyAI(AI):
    def move(self):
        col = randrange(0, 18)
        row = randrange(0, 18)
        return [col, row]
