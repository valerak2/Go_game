from abc import ABCMeta, abstractmethod


class AI:
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self):
        """Сделать ход"""
