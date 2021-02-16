import sys
from typing import Callable, Optional
from functools import wraps



def call_function_get_frame(func, *args, **kwargs):
    """
    https://stackoverflow.com/a/52358426/8851903
    Calls the function *func* with the specified arguments and keyword
    arguments and snatches its local frame before it actually executes.
    """

    frame = None
    trace = sys.gettrace()

    def snatch_locals(_frame, name, arg):
        nonlocal frame
        if frame is None and name == 'call':
            frame = _frame
            sys.settrace(trace)
        return trace
    sys.settrace(snatch_locals)
    try:
        result = func(*args, **kwargs)
    finally:
        sys.settrace(trace)
    return frame, result


def join(sep, iterable, mapper: Callable[[object], str] = str, except_values=(None,)):
    return sep.join(map(
        lambda v: '' if v in except_values else mapper(v),
        iterable
    ))


'''
import inspect
class once:
    """
        with once():
            # this code will run only once
            print(1)

        @once
        def _():
            # this code will run only once
            print(1)
    """

    __cache = {}

    def __init__(self, tag=None):
        if not tag:
            _locals = inspect.currentframe().f_back.f_locals
            if 'tag' not in _locals:
                raise SyntaxError('No "tag" in scope')
            tag = _locals['tag']
        self.tag = tag

    def __enter__(self):
        if self.tag in self.__cache:
            raise StopIteration('Code already run')
        else:
            self.__cache[self.tag] = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
'''


"""
class ChildrenComponent(list):
    def __new__(cls, args: Optional[list] = None):
        if args is None or args is False:
            return super().__new__(cls)
        try:
            if not isinstance(args, str) and len(args):
                if isinstance(args, ChildrenComponent):
                    return args
                return super().__new__(cls, args)
        except TypeError:
            pass
        super().__new__(cls, (args, ))

    def __repr__(self):
        return join('', self, repr)

    def __str__(self):
        return join('', self)
"""


class ChildrenComponent(list):
    def __init__(self, args: Optional[list] = None):
        if args is None or args is False:
            super().__init__()
            return
        try:
            if not isinstance(args, str) and len(args):
                super().__init__(args)
                return
        except TypeError:
            pass
        super().__init__((args, ))

    def __repr__(self):
        return join('', self, repr)

    def __str__(self):
        return join('', self)


class JSON(dict):
    def __getattr__(self, key: str) -> object:
        if key in dir(self):
            return super().__getattribute__(key)
        result = self.get(key)
        if type(result) is JSON:
            return result
        if type(result) is dict:
            return JSON(result)
        if isinstance(result, list) and len(result) and type(result[0]) == dict:
            return [JSON(value) for value in result]
        return result

    def __setattr__(self, key: str, value: object):
        if key in dir(self):
            return super().__setattr__(key, value)
        self[key] = value

    def __delattr__(self, key: str):
        if self.get(key) is not None:
            return self.pop(key)


"""
class state:
    # MAIN STATE

    _value = None

    def __init__(self, value):
        self._value = value

    def __get__(self):
        return self._value

    def __set__(self, value):
        self._value = value

    def __del__(self):
        self._value = None

    # END MAIN STATE
    # TYPE CAST METHODS

    def __int__(self):
        return int(self._value)

    def __str__(self):
        return str(self._value)

    def __iter__(self):
        return iter(self._value)

    # END TYPE CAST METHODS
    # COMPARE METHODS

    def __eq__(self, other):
        return self._value == other

    def __ne__(self, other):
        return self._value != other

    def __ge__(self, other):
        return self._value >= other

    def __gt__(self, other):
        return self._value > other

    def __le__(self, other):
        return self._value <= other

    def __lt__(self, other):
        return self._value < other

    # END COMPARE METHODS
    # ITEM METHODS

    def __getitem__(self, key):
        return self._value[key]

    def __setitem__(self, key, value):
        self._value[key] = value

    def __delitem__(self, key):
        del self._value[key]

    # END ITEM METHODS

    def __repr__(self):
        return f'state({self._value})'

    def __len__(self):
        return len(self._value)
"""


def __wrapper__(method):
    @wraps(method)
    def __wrapped_method__(self, *args, **kwargs):
        args = (
            arg.__get__() if hasattr(arg, '__get__') else arg
            for arg in args
        )
        kwargs = {
            name:
                value.__get__() if hasattr(value, '__get__') else value
            for name, value in kwargs.items()
        }

        return method(self, *args, **kwargs)

    return __wrapped_method__


class state:
    # MAIN STATE

    _value = None


    def __init__(self, value):
        self._value = value

    def __get__(self):
        return self._value

    def __set__(self, value):
        self._value = value

    def __del__(self):
        self._value = None

    # END MAIN STATE

    @__wrapper__
    def __getitem__(self, key):
        return self._value.__getitem__(key)

    @__wrapper__
    def __setitem__(self, key, value):
        return self._value.__setitem__(key, value)

    @__wrapper__
    def __delitem__(self, key):
        return self._value.__delitem__(key)

    # TODO: wrap getattribute if callable,
    #  to wrap arguments with .__get__() if available,
    #  because argument can be state

    # TODO: рими в комітах, щоб привернути увагу!!1!

    def __getattr__(self, key: str):
        if key == '_value' or key in dir(self):
            return super().__getattribute__(key)

        return self._value.__getattribute__(key)

    def __setattr__(self, key: str, value: object):
        if key == '_value' or key in dir(self):
            return super().__setattr__(key, value)
        return self._value.__setattr__(key, value)

    def __delattr__(self, key: str):
        if key == '_value' or key in dir(self):
            return super().__delattr__(key)
        return self._value.__delattr__(key)

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f'state({self._value})'

    def __len__(self):
        return len(self._value)
