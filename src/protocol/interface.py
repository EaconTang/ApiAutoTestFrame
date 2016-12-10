from abc import ABCMeta, abstractmethod, abstractproperty


class IConnection(object):
    """Connection interface for different connection in different protocol"""
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self.name = None

    @abstractmethod
    def send(self, *args, **kwargs):
        raise NotImplementedError

    @abstractproperty
    def response(self, *args, **kwargs):
        raise NotImplementedError


if __name__ == '__main__':
    pass