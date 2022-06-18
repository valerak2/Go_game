import unittest
from typing import TextIO

from game_module.logger import record_in_table, get_table_record
from gui.get_file_name import table_record_path


class MyTestCase(unittest.TestCase):
    def test_win(self):
        global old_value, new_value
        table = get_table_record()
        for i in table:
            if i[0] == 'test_player2':
                old_value = int(i[1])
        record_in_table("test_player2", None)
        table = get_table_record()
        for i in table:
            if i[0] == 'test_player2':
                new_value = int(i[1])
        self.assertFalse(old_value == new_value)
        self.assertTrue(old_value + 1 == new_value)

    def test_rating(self):
        file: TextIO = open(table_record_path(), "w", encoding='UTF-8')
        txt = "test_player1 1 0 0 \ntest_player2 0 0 0"

        file.truncate(0)
        file.write(txt)
        file.close()

        table = get_table_record()
        self.assertTrue(table[0][0] == "test_player1")
        self.assertTrue(table[1][0] == "test_player2")

        record_in_table("test_player2", None)
        record_in_table("test_player2", None)

        table = get_table_record()
        self.assertTrue(table[0][0] == "test_player2")
        self.assertTrue(table[1][0] == "test_player1")

if __name__ == '__main__':
    unittest.main()
