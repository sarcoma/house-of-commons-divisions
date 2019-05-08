from abc import ABCMeta, abstractmethod


class Transformer(metaclass=ABCMeta):

    @abstractmethod
    def get_data(self, data):
        pass
