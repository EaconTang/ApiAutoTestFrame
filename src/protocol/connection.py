from abc import ABCMeta, abstractmethod
import http


def get_conn(protocol_name):
    """register your new protocol implementation here"""
    _conn = {
        'http': http.HTTPConnection,
        'cm': None
    }.get(protocol_name, None)
    # if _conn:
    #     print _conn
    #     print IConnection
    #     print issubclass(_conn, IConnection)
    #     assert issubclass(_conn, IConnection), "Implementation class must inherit class IConnection!"
    return _conn


class IConnection(object):
    """Connection interface for different connection in different protocol"""
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = None

    @abstractmethod
    def send(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def response_dict   (self, *args, **kwargs):
        raise NotImplementedError


if __name__ == '__main__':
    print get_conn('cm')
