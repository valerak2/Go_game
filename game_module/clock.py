import datetime


class Clock:
    def __init__(self, time: datetime.time):
        self.clock = time
        self.basic_time = time

    def processing(self):
        if self.clock.second > 0:
            self.clock = datetime.time(self.clock.hour,
                                   self.clock.minute,
                                   self.clock.second - 1)
        elif self.clock.minute > 0:
            self.clock = datetime.time(self.clock.hour,
                                       self.clock.minute-1,
                                       59)
        elif self.clock.hour > 0:
            self.clock = datetime.time(self.clock.hour-1,
                                       59,
                                       59)
    def is_time_over(self):
        if self.clock.second == 0 and self.clock.minute == 0 and self.clock.hour == 0:
            return True
        else:
            return False

    def refresh(self):
        self.clock = self.basic_time

    def in_txt(self):
        return self.clock.strftime("%X")
