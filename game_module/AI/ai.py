from abc import ABCMeta, abstractmethod, abstractproperty


class AI():
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self):
        """Сделать ход"""
