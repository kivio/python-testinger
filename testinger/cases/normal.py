import inspect
from functools import wraps

def methodsWithDecorator(cls, decoratorName):
    result = []
    sourcelines = inspect.getsourcelines(cls)[0]
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decoratorName:
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            result.append(name)
    return result

class TestCase(object):

    _test_obj = None

    def setup(self):
        pass

    def clean(self):
        pass

    @property
    def test_obj(self):
        return self._test_obj

    def log(self, message):
        pass

    def fail(self, message):
        pass

    def main(self):
        case_methods = ['log','fail','main']
        tests =  [meth for meth in inspect.getmembers(self.__class__, predicate=inspect.ismethod)
                  if not meth[0] in case_methods and not meth[0].startswith('_')]

        no_tests = methodsWithDecorator(self.__class__, 'no_test')
        for name, test in tests:
            if not name in no_tests:
                self.__getattribute__(name)()

def raises(*args, **kwargs):
    pass

def step(message):
    def decor(function):
        @wraps(function)
        def dec(self, *args, **kwargs):
            return function(self, *args, **kwargs)
        return dec
    return decor

def no_test(function):
    @wraps(function)
    def decor(self, *args, **kwargs):
        return function(self, *args, **kwargs)
    return decor

class Mockup(object):

    def __init__(self, values):
        self.__dict__.update(values)

def scenario(scenarios):
    def decor(function):
        @wraps(function)
        def decorate(self, *args, **kwargs):
            args_l = inspect.getargspec(function)
            for scenario in scenarios:
                if len(args_l.args) > 1:
                    function(self, **scenario)
                else:
                    self.__dict__['_test_obj'] = Mockup(scenario)
                    function(self)
        return decorate
    return decor