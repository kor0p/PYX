from typing import Optional

from .core import join


class ChildrenComponent(list):
    def __init__(self, args: Optional[list] = None):
        if not args:
            super().__init__()
            return
        try:
            if not isinstance(args, str) and len(args):
                super().__init__(args)
                return
        except TypeError:
            pass
        super().__init__((args, ))

    def __hash__(self):
        return hash(tuple(self or ()))

    def __call__(self, *args, **kwargs):
        return ChildrenComponent([
            child(*args, **kwargs) if child else ''
            for child in self
        ])

    def __getattr__(self, key):
        if key in dir(self):
            return super().__getattribute__(key)
        return ChildrenComponent([
            getattr(child, key, '')
            for child in self
        ])

    def __repr__(self):
        return join('', self, repr)

    def __str__(self):
        return join('', self)

    def __iter__(self):
        r = super().__iter__()
        return r

    def __bool__(self):
        return len(self) > 0

    def __add__(self, other):
        this = self.copy()
        this.append(other)
        return this

    def __radd__(self, other):
        this = self.copy()
        this.insert(0, other)
        return this
