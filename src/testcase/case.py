import json


class Case(object):
    """Test case class"""

    def __init__(self, file_path):
        self.case_path = str(file_path)
        with open(self.case_path) as f:
            case_str = f.read()
        self.case_str = case_str

    @property
    def case_type(self):
        if self.case_path.endswith('json'):
            return 'json'
        if self.case_path.endswith('yaml') or self.case_path.endswith('yml'):
            return 'yaml'
        if self.case_path.endswith('xls') or self.case_path.endswith('xlsx'):
            return 'excel'
        raise TypeError('Unsupported file type!')

    @property
    def case_dict(self):
        """parse case text to dict"""
        return {
            'json': json.loads(self.case_str),
            'yaml': {},
            'excel': self.excel_to_dict(),
        }.get(self.case_type, {})

    def excel_to_dict(self):
        return {}
