import sys

from src.testcase.case import Case
from src.precondition import *
from src.protocol.register import get_conn
from src.utils import trans_type, check_dependency
from src.db.client import get_mysql_conn
from src.db.orm_table import InsertTable


def main():
    """"""
    # load testcase
    case = Case('/Users/eacon/github/APIAutoTestFramework/case/sample.json')
    # check preconditions
    pre = case.case_dict.get('precondition')
    if pre:
        # pre functions
        func_list = pre.get('prefunction')
        for func in func_list:
            _func = eval(func.get('func_name'))
            _args = {_.get('name'): trans_type(_.get('value'), _.get('type')) for _ in func.get('args')}
            _func(**_args)
        # dependency
        check_dependency(pre.get('dependency'))

    # steps
    for step in case.case_dict.get('step'):
        # input
        _input = step.get('input')
        res = {}
        for protocol, _args in _input.iteritems():
            req = get_conn(protocol)(**_args)
            res = req.response
        # compare output
        _output = step.get('output')
        if _output.get('strict'):
            # ToDo
            pass
        try:
            for _ in _output.get('expect'):
                _var = _.get('var')
                _expect_value = trans_type(_['val']['value'], _['val']['type'])
                _real_value = res.get(_var)
                if _.get('cmp') == '==':
                    assert _expect_value == _real_value, "Not equal! \n\tExpect: {}\n\tGot: {}".format(_expect_value, _real_value)
        except AssertionError as e:
            sys.stderr.write(e.message)
            PASS = False
        else:
            PASS = True

    # subsequent operations
    # record to mysql
    return PASS


if __name__ == '__main__':
    print main()