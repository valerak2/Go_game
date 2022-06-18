import datetime
import unittest

from game_module.clock import Clock


class MyTestCase(unittest.TestCase):
    def test_clock(self):
        timer = datetime.time(0, 0, 2)
        clock = Clock(timer)

        clock.processing()
        self.assertFalse(clock.is_time_over())

        clock.processing()
        self.assertTrue(clock.is_time_over())

        clock.refresh()
        self.assertTrue(clock.in_txt() == "00:00:02")
        self.assertFalse(clock.is_time_over())


if __name__ == '__main__':
    unittest.main()
