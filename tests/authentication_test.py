import unittest
from typing import TextIO
from gui.get_file_name import table_record_path
from gui.menu.authentication import Authentication


class MyTestCase(unittest.TestCase):
    def test_logic(self):
        file: TextIO = open(table_record_path(), "w", encoding='UTF-8')
        txt = "test_player1 1 0 0 \ntest_player2 0 0 0"

        file.truncate(0)
        file.write(txt)
        file.close()

        a = Authentication()
        self.assertTrue(a.users[0] == "test_player1")
        self.assertTrue(a.users[1] == "test_player2")

        self.assertTrue(a.correct_name("test_player1"))
        self.assertFalse(a.correct_name("test_player3"))

        self.assertFalse(a.correct_new_name("test_player1"))
        self.assertTrue(a.correct_new_name("test_player3"))


if __name__ == '__main__':
    unittest.main()
