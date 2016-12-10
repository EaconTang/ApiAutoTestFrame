from src.protocol.http import HTTPConnection


def get_conn(protocol_name):
    """register your new protocol implementation here"""
    _conn = {
        'http': HTTPConnection,
        'cm': None
    }.get(protocol_name, None)
    # if _conn:
    #     print _conn
    #     print IConnection
    #     print issubclass(_conn, IConnection)
    #     assert issubclass(_conn, IConnection), "Implementation class must inherit class IConnection!"
    return _conn
