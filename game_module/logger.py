from typing import TextIO


class Logger:
    def __init__(self):
        self.log: TextIO = open("../gui/party_log.txt", "r+", encoding='cp1251')
        self.log.truncate(0)
        self.log.write("История ходов:" + "\n")

    def write(self, txt: str):
        self.log.write(txt + "\n")

    def close(self):
        self.log.close()

    def record_in_table(self, color, AI):
        table: TextIO = open("../gui/table_record.txt", "r", encoding='cp1251')
        txt = table.read().split("\n")
        table.close()

        if color:
            if AI is None:
                # белый выйграл
                i = 1
            else:
                # бот выйграл
                i = 2
        else:
            # игрок победил
            i = 0

        old = txt[i].split(":")
        new = old[0] + ": " + str(int(old[1]) + 1)
        txt[i] = new

        table: TextIO = open("../gui/table_record.txt", "w", encoding='cp1251')
        table.truncate(0)
        for j in txt:
            table.write(j + "\n")
        table.close()