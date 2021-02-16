import inspect
from functools import wraps
from typing import Union, Callable

from .utils import call_function_get_frame, ChildrenComponent, JSON, state

__requests__ = {}
__DOM__ = {}


class Tag(JSON):
    f = None
    k = {}
    children = ''
    _cached = {}

    def __len__(self):
        return 0

    def __bool__(self):
        return bool(self.f)

    @property
    def name(self):
        return self._options.get('name')

    @name.setter
    def name(self, name):
        self._options['name'] = name

    def update(self, **k):
        cls = type(self)

        @wraps(cls)
        def _tag(f):
            return cls(f, **(self._options | k))
        return _tag

    def __new__(cls, f=None, *, name='', cache=False, is_in_dom=True, **k):
        if isinstance(f, cls):
            return f
        self = super().__new__(cls)

        self._options = JSON(
            name=name or (f.__name__ if f else ''),
            cache=cache,
            is_in_dom=is_in_dom,
            **k,
        )

        self.f = Component(f)
        self.f.__tag__ = self

        return self

    def __init__(self, *a, **k):
        super().__init__()

    def __hash__(self):
        return hash((self.name, hash(self.f)))

    def _get_cached_key(self, kwargs: JSON):
        return (
            self.name,
            hash(self.f),
            tuple(sorted((a, str(b)) for a, b in kwargs.items()))
        )

    def clone(self):
        cls = type(self)
        return cls(
            self.f,
            **self._options,
        )

    def __call__(self, *a, **k):
        if a:
            return self.update()(*a)
        k = self.k | k
        k = JSON(k)
        is_cached = self._options.get('cache')
        cached_key = None
        if is_cached:
            cached_key = self._get_cached_key(k)
            if cached := self._cached.get(cached_key):
                # print(cached.children)
                return cached
        if 'children' in k:
            k['children'] = ChildrenComponent(k['children'])
        this = self.clone()
        this.f.kw = k
        tag_arguments = inspect.getfullargspec(this.f._f)
        is_class_component = isinstance(this.f._f, type)
        if len(tag_arguments.args) == is_class_component:
            this.children = this.f(**k)
        elif 'tag' in k:
            this.children = this.f(this.f, **k)
        else:
            this.children = this.f(tag=this.f, **k)
        # this.children = this.f(**k)

        _attrs = JSON()
        for k, v in k.items():
            if callable(v):
                # k = k.lower()
                _hash = hash(v)
                _key = self.name + '___' + k + '___' + str(_hash)
                __requests__[_key] = v
                v = _hash
            _attrs[k] = v
        this.f.kw = this.k = _attrs
        # print(this.name, this.children, repr(this.children))
        if is_cached:
            self._cached[cached_key] = this
        return this

    def __repr__(self):
        return str(self.name) + '(' + ', '.join(str(k) + '=' + str(v) for k, v in self.k.items()) + ')'

    def __str__(self):
        if fn := getattr(self.f, '__render__', None):
            return str(fn(self))
        _hash = hash(self)
        __DOM__[str(_hash)] = self

        attrs = self.k.copy()
        attrs['pyx-id'] = _hash
        if self._options.is_in_dom:
            attrs['pyx-dom'] = True
        if 'children' in attrs:
            children = attrs.pop('children')
        else:
            children = ''

        r = '<' + self.name
        for k, v in attrs.items():
            if v is None or v is False:
                continue
            if v is True:
                r += ' ' + k
                continue
            r += ' ' + k + '="' + str(v) + '"'
        r += f'>{self.children}</{self.name}>'
        return r
        # return str(self.children)


class Component:
    _f: Callable = None
    __tag__: Tag = None
    kw: JSON = JSON()
    frame = None
    locals: dict = {}
    _state_cls = state

    def __new__(cls, f):
        if isinstance(f, cls):
            return f
        self = super().__new__(cls)

        if f and hasattr(f, '__globals__'):
            f.__globals__.update(dict(self=self))
        self._f = f
        self.kw = JSON()

        return self

    def __init__(self, *a, **k):
        super().__init__()

    def __str__(self):
        return (
            '<Component ' + self._f.__name__ + '('
            + ', '.join(k + '=' + v for k, v in self.kw.items())
            + ')>'
        )

    def __hash__(self):
        return hash((
            self._f,
            self.__name__,
            self._state_cls,
        ))

    def __call__(self, *a, **k):
        f = self._f
        if not f or not callable(f):
            return
        frame, result = call_function_get_frame(f, *a, **k)
        self._f.frame = frame
        self._f.locals = frame.f_locals
        return ChildrenComponent(result)

    def __getattr__(self, key, raw=False):
        _value = None
        if key in dir(self._f):
            _value = getattr(self._f, key, _value)
        else:
            try:
                _value: Union[state, object] = super().__getattribute__(key)
            except AttributeError:
                pass
        if raw:
            return _value
        if key in dir(self):
            return _value

        if isinstance(_value, self._state_cls):
            return _value.__get__()
        return _value

    def __setattr__(self, key, value):
        if key in dir(self):
            return super().__setattr__(key, value)

        _state_cls = self._state_cls
        _exists_value: Union[state, object] = self.__getattr__(key, raw=True)

        if isinstance(value, _state_cls):
            if isinstance(_exists_value, _state_cls):
                return
            else:
                return self._f.__setattr__(key, value)
        else:
            if isinstance(_exists_value, _state_cls):
                return _exists_value.__set__(value)
            else:
                return self._f.__setattr__(key, value)

    def __delattr__(self, key):
        if key in dir(self):
            return super().__delattr__(key)

        _exists_value: Union[state, object] = self.__getattr__(key, raw=True)

        if isinstance(_exists_value, self._state_cls):
            return _exists_value.__del__()
        else:
            return self._f.__delattr__(key)


# cached_tag = Tag(cache=True)
cached_tag = Tag(cache=False)

