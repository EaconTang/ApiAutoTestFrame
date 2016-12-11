from src.testcase.case import Case
from src.utils import *
from src.protocol.register import get_conn
from src.precondition import *


class OneCase(object):
    """
    Main flow of running one case's autotest
    """
    PASS = True
    FAIL = False

    def __init__(self, case_path, *args, **kwargs):
        self._case_path = str(case_path)
        self._case_dict = {}
        self._step_result = []
        self._step_msg = []
        self._passed = False

    def run(self):
        self.load_case(self._case_path)
        self.satisfy_precondition(self._case_dict)
        self.exec_steps(self._case_dict)
        self.save_result()

    def load_case(self, case_path):
        self._case_dict = Case(file_path=case_path).case_dict

    def satisfy_precondition(self, case_dict):
        pre = case_dict.get('precondition')
        if pre:
            # pre functions
            func_list = pre.get('prefunction')
            for func in func_list:
                _func = eval(func.get('func_name'))
                _args = {_.get('name'): trans_type(_.get('value'), _.get('type')) for _ in func.get('args')}
                _func(**_args)
            # dependency
            check_dependency(pre.get('dependency'))

    def check_dependency(self):
        pass    # ToDo

    def exec_steps(self, case_dict):
        """
        """
        for step in case_dict.get('step'):
            # input
            _input = step.get('input')
            res = {}
            for protocol, _args in _input.iteritems():
                req = get_conn(protocol)(**_args)
                res = req.response
            # compare output
            _output = step.get('output')
            if _output.get('strict'):
                pass    # ToDo
            try:
                for _ in _output.get('expect'):
                    _var = _.get('var')
                    _expect_value = trans_type(_['val']['value'], _['val']['type'])
                    _real_value = res.get(_var)
                    if _.get('cmp') == '==':
                        assert _expect_value == _real_value, "Not equal! \n\tExpect: {}\n\tGot: {}".format(
                            _expect_value, _real_value)
            except AssertionError as e:
                self._step_result.append(self.FAIL)
                self._step_msg.append(e.message)
            else:
                self._step_result.append(self.PASS)
                self._step_msg.append('Passed!')
        self._passed = all(self._step_result)

    def save_result(self):
        """
        save result for this test
        1) print to console
        2) record to mysql
        3) upload to testlink
        """
        self.print_to_console()

    def print_to_console(self):
        if self._passed:
            print('All steps passed for case: {}'.format(self._case_dict.get('name')))
        else:
            err('Failed on case: {}'.format(self._case_dict.get('name')))
            step_length = range(1, len(self._step_result) + 1)
            for i, result, msg in zip(step_length, self._step_result, self._step_msg):
                if result == self.FAIL:
                    err('Step {} failed for reason:\n\t{}'.format(i, msg))


if __name__ == '__main__':
    testcase = OneCase('/Users/eacon/github/APIAutoTestFramework/case/sample.json')
    testcase.run()