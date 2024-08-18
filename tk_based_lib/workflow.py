import functools

class Wrap():
    @classmethod
    def as_function_node(self, label):
        def decoratorInner(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                out = func(self, *args, **kwargs)
                print(out,'Steffen')
            return wrapper
        return decoratorInner


class Workflow():
    wrap = Wrap
    def __init__(self, path) -> None:
        print(path,"TODO More")

    def run(self):
        return {'key':'here I have to create more'}

    def draw(self):
        """ Dummy method to mimic pyiron-workflow"""
        obj = Picture()
        return obj


class Picture():
    """ Dummy picture class that does nothing than create a file that pyiron-workflow also creates """
    def __init__(self) -> None:
        pass
    def render(self, filename='', format=''):
        with open(filename, 'w', encoding='utf-8') as fOut:
            fOut.write('Dummy method\n')
