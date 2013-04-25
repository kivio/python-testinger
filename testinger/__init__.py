import inspect

from cases.normal import TestCase

ours = ['TestCase', 'WebTestCase']

def main():
    module = __import__('__main__')
    for element in [el for el in dir(module) if not el in ours]:
        elf = getattr(module, element)
        if inspect.isclass(elf):
            print('Run scenarios for: {}'.format(getattr(elf, '__stage__', element)))
            cls = elf()
            cls.main()
