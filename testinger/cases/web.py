from functools import wraps

from normal import TestCase

def client(path, mime = 'text'):
    def decor(function):
        @wraps(function)
        def dec(self, *args, **kwargs):
            return function(self, *args, **kwargs)
        return dec
    return decor

class WebTestCase(TestCase):

    @property
    def status_code(self):
        return 200

    @property
    def data(self):
        return {'success' : 'data has sended'}

    @property
    def client(self):
        return None