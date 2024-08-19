import functools

#global variable to store output of functions
data = []

class Wrap():
    """ Wrapper class that defines the decorator """
    def as_function_node(self, _):
        """ decorator function """
        def decoratorInner(func):
            """ inner decorator, that is returned """
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                # wrapper that can access the local variables of the wrapped function
                out = func(self, *args, **kwargs)
                data.append(out)
            return wrapper
        return decoratorInner


class Workflow():
    """ Boilerplate = minimalistic workflow engine"""
    wrap = Wrap()

    def __init__(self, *args, **kwargs) -> None:
        pass

    def run(self):
        """ executed at end to return all the workflow step output """
        res = {}
        for idx, out in enumerate(data):
            res[f'step{idx+1}__y'] = out
        return res

    def draw(self):
        """ Dummy method to mimic pyiron-workflow"""
        obj = Picture()
        return obj


class Picture():
    """ Dummy picture class that does nothing than create a file that pyiron-workflow also creates """
    def render(self, filename='', format=''):
        with open(filename, 'w', encoding='utf-8') as fOut:
            fOut.write('Dummy method\n')
