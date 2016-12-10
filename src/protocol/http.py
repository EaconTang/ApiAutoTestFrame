from src.protocol.interface import IConnection
import requests


class HTTPConnection(IConnection):
    def __init__(self, url=None, ip=None, port=None, path=None, method='GET', param=None):
        """
        params in case-file: "step->input->http"
        Either 'url' or 'ip' + 'port' + 'path' is required.
        :param url:
        :param ip:
        :param port:
        :param path:
        :param method:
        :param param:
        """
        self.name = 'http'
        self.ip = ip
        self.port = port
        self.path = path
        if url:
            if str(url).startswith('http://'):
                self.url = url
            else:
                self.url = 'http://{}'.format(url)
        else:
            self.url = 'http://{}:{}{}'.format(self.ip, self.port, self.path)
        self.method = str(method)
        self.param = param
        self._response = None
        self.sent_success = False

    @property
    def prepared_request(self):
        req = requests.Request(method=self.method.upper(), url=self.url, params=self.param)
        return req.prepare()

    @property
    def session(self):
        return requests.Session()

    def send(self):
        """"""
        with self.session as s:
            self._response = s.send(self.prepared_request)
        self.sent_success = True

    def get_response(self):
        if not self.sent_success:
            self.send()
        return self._response

    @property
    def response(self):
        """
        keys in this dict, could be used in case-file: "step->output->match->vars"
        all keys: ['code', 'content',
                    'cookies', '_content', 'headers', 'url', 'status_code', '_content_consumed',
                    'encoding', 'request', 'connection', 'elapsed', 'raw', 'reason', 'history',
                    ]
        :return:
        """

        _dict = self.get_response().__dict__
        code, content = _dict.get('status_code'), _dict.get('_content')
        _dict.update(code=code, content=content)
        return _dict


if __name__ == '__main__':
    pass
