# from connection import IConnection
import requests


class HTTPConnection(object):
    def __init__(self, url=None, ip=None, port=None, path=None, method='GET', param=None):
        """
        params in case-file: "step->input->http"
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
        req = requests.Request(method=self.method.upper(), url=self.url)
        return req.prepare()

    def send(self):
        with requests.Session() as s:
            self._response = s.send(self.prepared_request)
        self.sent_success = True

    @property
    def response(self):
        if not self.sent_success:
            self.send()
        return self._response

    @property
    def response_dict(self):
        """
        keys in this dict, could be used in case-file: "step->output->match->vars"
        :return:
        """
        # keys: ['cookies', '_content', 'headers', 'url', 'status_code', '_content_consumed', 'encoding', 'request', 'connection', 'elapsed', 'raw', 'reason', 'history']
        _dict = self.response.__dict__
        code, content = _dict.get('status_code'), _dict.get('_content')
        _dict.update(dict(code=code, content=content))
        return _dict


if __name__ == '__main__':
    print HTTPConnection('www.baidu.com').response_dict['content']
