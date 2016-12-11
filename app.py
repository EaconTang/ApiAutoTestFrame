import os
from src import task


def main():
    """"""
    _case_path = os.path.join(os.path.dirname(__file__), 'case', 'sample.json')
    testcase =task.OneCase(case_path=_case_path)
    testcase.run()

    # output:

    # onSuccess:
    #   All steps passed for case: test

    # onFail:
    #   Failed on case: test
    #   Step 1 failed for reason:
    #       Not equal!
    #       Expect: 201
    #       Got: 200

if __name__ == '__main__':
    main()