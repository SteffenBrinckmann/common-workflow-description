""" Minimalistic workflow """
import functools
from inspect import signature

class RShiftableOutput:
    """ Output of the wrapper / decorator function """
    def __init__(self, value):
        self.value = value

    def __rshift__(self, other):
        return other


class WorkflowOutputs(dict):
    """ Output of the entire workflow """
    def to_value_dict(self):
        """ return workflow output as dictionary """
        return self


class Wrap():
    """ Wrapper class that defines the decorator """
    def as_function_node(self, _):
        """ decorator function """
        def decorator_inner(func):
            """ inner decorator, that is returned """
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                wrapped_params = signature(func).parameters
                kwargs = {k: v for k, v in kwargs.items() if k in wrapped_params}
                # wrapper that can access the local variables of the wrapped function
                out = func(self, *args, **kwargs)
                return RShiftableOutput(out)
            return wrapper
        return decorator_inner


class Workflow():
    """ Boilerplate = minimalistic workflow engine"""
    wrap = Wrap()

    def __init__(self, *args, **kwargs) -> None:
        self.outputs = WorkflowOutputs()

    def draw(self):
        """ Dummy method to mimic pyiron-workflow"""
        obj = Picture()
        return obj

    def __setattr__(self, key, value):
        if isinstance(value, RShiftableOutput):
            self.outputs[key] = value.value
        super().__setattr__(key, value)


class Picture():
    """ Dummy picture class that does nothing """
    def render(self, *args, **kwargs):
        """ render the workflow as a picture """
