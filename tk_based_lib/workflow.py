import functools
from inspect import signature

#global variable to store output of functions
data = []


class RShiftableOutput:
    def __init__(self, value):
        self.value = value

    def __rshift__(self, other):
        print(f"{self} ({id(self)}) ignoring rshift to {other} ({id(other)})")
        return other


class Wrap():
    """ Wrapper class that defines the decorator """
    def as_function_node(self, _):
        """ decorator function """
        def decoratorInner(func):
            """ inner decorator, that is returned """
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                wrapped_params = signature(func).parameters
                kwargs = {k: v for k, v in kwargs.items() if k in wrapped_params}

                # wrapper that can access the local variables of the wrapped function
                out = func(self, *args, **kwargs)
                data.append(out)
                return RShiftableOutput(out)
            return wrapper
        return decoratorInner

class _LikePyironWorkflowOutputs(dict):
    def to_value_dict(self):
        return self


class Workflow():
    """ Boilerplate = minimalistic workflow engine"""
    wrap = Wrap()

    def __init__(self, *args, **kwargs) -> None:
        self.outputs = _LikePyironWorkflowOutputs()

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

    def __setattr__(self, key, value):
        if isinstance(value, RShiftableOutput):
            self.outputs[key] = value.value
        super().__setattr__(key, value)


class Picture():
    """ Dummy picture class that does nothing than create a file that pyiron-workflow also creates """
    def render(self, filename='', format='', **kwargs):
        with open(filename, 'w', encoding='utf-8') as fOut:
            fOut.write('Dummy method\n')
