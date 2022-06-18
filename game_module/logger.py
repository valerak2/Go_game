from typing import TextIO

from game_module import AI
from game_module.AI.easy_AI import EasyAI
from game_module.AI.medium_AI import MediumAI
from gui.get_file_name import party_log_path, table_record_path


def record_in_table(name, game_mode: AI):
    table: TextIO = open(table_record_path(), "r", encoding='UTF-8')
    txt = table.read().split("\n")
    table.close()
    count = 0
    for i in txt:
        res = i.split(' ')
        if res[0] == name:
            if game_mode is None:
                index_res = 1
            if isinstance(game_mode, EasyAI):
                index_res = 2
            if isinstance(game_mode, MediumAI):
                index_res = 3
            point = int(res[index_res]) + 1
            res[index_res] = str(point)
            new_res = ''
            for j in range(len(res)):
                new_res += res[j] + ' '
            txt[count] = new_res
        count += 1
    table: TextIO = open(table_record_path(), "w", encoding='UTF-8')
    table.truncate(0)
    for i in txt:
        table.write(i + "\n")
    table.close()


def get_table_record():
    file: TextIO = open(table_record_path(), "r", encoding='UTF-8')
    table = []
    for i in file.readlines():
        split = i.replace('\n', '').split(" ")
        if split.__len__() < 4:
            continue
        name = split[0]
        win_hotseat = split[1]
        win_easy_AI = split[2]
        win_medium_AI = split[3]
        sum_win_point = int(win_hotseat) + int(win_easy_AI) + int(win_medium_AI)
        table.append([name,
                      win_hotseat,
                      win_easy_AI,
                      win_medium_AI,
                      sum_win_point
                      ])
    file.close()
    return sorted(table, key=lambda x: x[4], reverse=True)


class Logger:
    def __init__(self):
        self.log: TextIO = open(party_log_path(), "r+", encoding='UTF-8')
        self.log.truncate(0)
        self.log.write("История ходов:" + "\n")

    def write(self, txt: str):
        self.log.write(txt + "\n")

    def close(self):
        self.log.close()
