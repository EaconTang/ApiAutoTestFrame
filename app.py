from src import testcase


if __name__ == '__main__':
    case = testcase.Case('/Users/eacon/github/APIAutoTestFramework/case/sample.json')
    print(case.case_dict.get('comment'))