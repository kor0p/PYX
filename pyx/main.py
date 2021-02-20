import inspect
from functools import wraps
from typing import Union, Callable, TypeVar

from .utils import call_function_get_frame, ChildrenComponent, JSON, state

__requests__ = {}
__DOM__ = {}
T = TypeVar('T', bound='Tag')


def get_from_dom(tag: T):
    return __DOM__.get(str(hash(tag)))


def set_to_dom(key_or_value, value=None):
    if value:
        __DOM__[str(key_or_value)] = value
    else:
        __DOM__[str(hash(key_or_value))] = key_or_value


class ClassComponent:
    __render__: Callable


class Tag(JSON):
    f = None
    kw = {}
    children: Union[ChildrenComponent[str, ClassComponent]] = ''
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

    def update(self, **k) -> Callable[[Callable], T]:
        cls = type(self)

        @wraps(cls)
        def _tag(f):
            return cls(f, **(self._options | k))

        _tag.update = lambda **_k: self.update(**(k | _k))
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
        return hash((self.name, self.f, tuple(self.kw.items())))

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

    def __call__(self, *a: tuple[Callable], **kw: dict[str, object]):
        """
        @Tag()
        def custom_tag():
            pass

        cached_tag = Tag(cache=True)
        @cached_tag.update(name='test')
        def custom_tag(tag):
            pass

        @Tag()
        def custom_tag():
            pass
        """
        if a:
            return self.update()(*a)
        kw = self.kw | kw
        kw = JSON(kw)
        is_cached = self._options.get('cache')
        cached_key = None
        if is_cached:
            cached_key = self._get_cached_key(kw)
            if cached := self._cached.get(cached_key):
                return cached
        if '_class' in kw:
            kw['class'] = kw.pop('_class')
        if self._options.get('children_raw', False) and 'children' in kw:
            kw['children'] = ChildrenComponent(kw['children'])

        this = self.clone()
        this.f.kw = this.kw = kw
        tag_arguments = inspect.getfullargspec(this.f._f)
        is_class_component = isinstance(this.f._f, type)
        if len(tag_arguments.args) == is_class_component:
            this.children = this.f(**kw)
        elif 'tag' in kw:
            this.children = this.f(this.f, **kw)
        else:
            this.children = this.f(tag=this.f, **kw)

        _attrs = JSON()
        for k, v in kw.items():
            if callable(v) and not isinstance(v, ChildrenComponent):
                _hash = hash(v)
                _key = this.name + '___' + k + '___' + str(_hash)
                __requests__[_key] = v
                v = _hash
            _attrs[k] = v
        this.f.kw = this.kw = _attrs
        if is_cached:
            self._cached[cached_key] = this
        return this

    def __repr__(self):
        return str(self.name) + '(' + ', '.join(str(k) + '=' + str(v) for k, v in self.kw.items()) + ')'

    def __str__(self):
        _hash = hash(self)
        set_to_dom(_hash, self)

        if getattr(self.f, '__render__', None) is not None:
            r = str(self.children.__render__(self))
        else:
            attrs = self.kw.copy()
            if 'children' in attrs:
                attrs.pop('children')

            r = '<' + self.name
            for k, v in attrs.items():
                if v is None or v is False:
                    continue
                if v is True:
                    r += ' ' + k
                    continue
                r += ' ' + k + '="' + str(v) + '"'
            r += '>'
            if not self._options.get('_void_tag', False):
                r += f'{self.children}</{self.name}>'

        r = r.replace(
            '<' + self.name,
            f'<{self.name} pyx-id="{_hash}" ' + ('pyx-dom ' if self._options.is_in_dom else ''),
            1
        )
        return r


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
        return ChildrenComponent(f(*a, **k))
        """
        frame, result = call_function_get_frame(f, *a, **k)
        self._f.frame = frame
        self._f.locals = frame.f_locals
        return ChildrenComponent(result)
        """

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

