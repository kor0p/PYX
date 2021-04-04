from functools import wraps


def __wrapper__(method):
    @wraps(method)
    def __wrapped_method__(self, *args, _raw=False, **kwargs):
        if not _raw:
            args = (arg.__get__() if hasattr(arg, '__get__') else arg for arg in args)
            kwargs = {name: value.__get__() if hasattr(value, '__get__') else value for name, value in kwargs.items()}

        return method(self, *args, **kwargs)

    return __wrapped_method__


class state:
    # MAIN STATE

    _value_init = ...  # state(None) must handle None initial value
    _value = None
    _name = ''

    def __init__(self, value=None, name=''):
        self.__set__(value)
        self._name = name

    def __get__(self):
        return self._value

    def _set(self, value):
        self._value = value

    def __set__(self, value):
        self._set(value)
        if self._value_init is ...:
            self._value_init = value

    def __del__(self):
        self._value = None

    def __get_init__(self):
        return self._value_init

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

    # TYPE CAST METHODS

    def __int__(self):
        return int(self._value)

    def __str__(self):
        return str(self._value)

    def __abs__(self):
        return abs(self._value)

    def __complex__(self):
        return complex(self._value)

    def __round__(self):
        return round(self._value)

    def __float__(self):
        return float(self._value)

    def __oct__(self):
        return oct(self._value)

    def __hex__(self):
        return hex(self._value)

    def __iter__(self):
        return iter(self._value)

    # END TYPE CAST METHODS
    # COMPARISON METHODS

    @__wrapper__
    def __eq__(self, other):
        return self._value == other

    @__wrapper__
    def __ne__(self, other):
        return self._value != other

    @__wrapper__
    def __ge__(self, other):
        return self._value >= other

    @__wrapper__
    def __gt__(self, other):
        return self._value > other

    @__wrapper__
    def __le__(self, other):
        return self._value <= other

    @__wrapper__
    def __lt__(self, other):
        return self._value < other

    # END COMPARISON METHODS
    # UNARY METHODS

    def __neg__(self):
        return -self._value

    def __pos__(self):
        return +self._value

    def __invert__(self):
        return ~self._value

    # END UNARY METHODS
    # ARITHMETIC METHODS

    @__wrapper__
    def __add__(self, other):
        return self._value + other

    @__wrapper__
    def __sub__(self, other):
        return self._value - other

    @__wrapper__
    def __mul__(self, other):
        return self._value * other

    @__wrapper__
    def __floordiv__(self, other):
        return self._value // other

    @__wrapper__
    def __div__(self, other):
        return self._value / other

    @__wrapper__
    def __mod__(self, other):
        return self._value % other

    @__wrapper__
    def __pow__(self, other):
        return self._value ** other

    @__wrapper__
    def __lshift__(self, other):
        return self._value << other

    @__wrapper__
    def __rshift__(self, other):
        return self._value >> other

    @__wrapper__
    def __and__(self, other):
        return self._value & other

    @__wrapper__
    def __or__(self, other):
        return self._value | other

    @__wrapper__
    def __xor__(self, other):
        return self._value ^ other

    # END ARITHMETIC METHODS
    # REFLECTED ARITHMETIC METHODS

    @__wrapper__
    def __radd__(self, other):
        return other + self._value

    @__wrapper__
    def __rsub__(self, other):
        return other - self._value

    @__wrapper__
    def __rmul__(self, other):
        return other * self._value

    @__wrapper__
    def __rfloordiv__(self, other):
        return other // self._value

    @__wrapper__
    def __rdiv__(self, other):
        return other / self._value

    @__wrapper__
    def __rmod__(self, other):
        return other % self._value

    @__wrapper__
    def __rpow__(self, other):
        return other ** self._value

    @__wrapper__
    def __rlshift__(self, other):
        return other << self._value

    @__wrapper__
    def __rrshift__(self, other):
        return other >> self._value

    @__wrapper__
    def __rand__(self, other):
        return other & self._value

    @__wrapper__
    def __ror__(self, other):
        return other | self._value

    @__wrapper__
    def __rxor__(self, other):
        return other ^ self._value

    # END REFLECTED ARITHMETIC METHODS
    # AUGMENTED ASSIGMENT METHODS

    @__wrapper__
    def __iadd__(self, other):
        self._set(self._value + other)

    @__wrapper__
    def __isub__(self, other):
        self._set(self._value - other)

    @__wrapper__
    def __imul__(self, other):
        self._set(self._value * other)

    @__wrapper__
    def __ifloordiv__(self, other):
        self._set(self._value // other)

    @__wrapper__
    def __idiv__(self, other):
        self._set(self._value / other)

    @__wrapper__
    def __imod__(self, other):
        self._set(self._value % other)

    @__wrapper__
    def __ipow__(self, other):
        self._set(self._value ** other)

    @__wrapper__
    def __ilshift__(self, other):
        self._set(self._value << other)

    @__wrapper__
    def __irshift__(self, other):
        self._set(self._value >> other)

    @__wrapper__
    def __iand__(self, other):
        self._set(self._value & other)

    @__wrapper__
    def __ior__(self, other):
        self._set(self._value | other)

    @__wrapper__
    def __ixor__(self, other):
        self._set(self._value ^ other)

    # END AUGMENTED ASSIGMENT METHODS

    def __repr__(self):
        return f'state<{self._name or "anon"}>({self._value}, init={self._value_init})'

    def __len__(self):
        return len(self._value)
