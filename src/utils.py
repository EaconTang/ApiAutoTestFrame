import os
import sys


def err(msg):
    """"""
    print >> sys.stderr, msg


def check_dependency(dependency_list):
    """check whether the dependent apis are ok"""
    # ToDO
    pass


def trans_type(_value, _type):
    """trans value to specified type"""
    if _type == 'int':
        return int(_value)
    if _type == 'string':
        return str(_value)
    return _value


def walk_dir(dir_path):
    """

    :param dir_path:
    :return:
    """
    os.walk()


if __name__ == '__main__':
    err('hello')
    err('world')