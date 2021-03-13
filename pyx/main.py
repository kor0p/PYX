import inspect
from functools import wraps
from typing import Union, Callable, TypeVar
from types import ModuleType

from .utils import escape, ChildrenComponent, JSON, state, set_to_dom, get_session_id
from .utils.app import create_request

T = TypeVar('T', bound='Tag')


class ClassComponent:
    __render__: Callable


class PYXModule(ModuleType):
    __pyx__: Callable


class Tag:
    f = None
    kw = {}
    hash = None
    session = None
    children: Union[ChildrenComponent[str, ClassComponent]] = ''
    _cached = {}
    _options: JSON = JSON()
    __name__ = None  # uses for class components

    def __len__(self):
        return 0

    def __bool__(self):
        return bool(self.f)

    def extend(self, **options):
        return dict(metaclass=MetaTag) | self._options | options

    def __add__(self, other):
        return ChildrenComponent([self, other])

    @property
    def init(self):
        """
        def pyx(tag):
            if tag.init:
                print('inited')
            return ''
        """
        return self._options.get('init')

    @property
    def name(self):
        return self.__name__ or self._options.get('title')

    @name.setter
    def name(self, name):
        self._options['title'] = name

    def update(self, **k) -> Callable[[Callable], T]:
        cls = type(self)

        @wraps(cls)
        def _tag(f):
            return cls(f, **(self._options | k))

        _tag.update = lambda **_k: self.update(**(k | _k))
        return _tag

    def __new__(cls, f=None, *, title='', cache=False, is_in_dom=True, init=True, escape=True, **k):
        if isinstance(f, cls):
            return f
        self = super().__new__(cls)

        self._options = self._options | JSON(
            cache=cache,
            is_in_dom=is_in_dom,
            init=init,
            escape=escape,
            **k,
        )

        self.name = title or (f.__name__ if f else '')

        self.f = Component(f)
        self.f.__tag__ = self
        try:
            self.session = get_session_id()
        except RuntimeError:
            pass

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
            self.f.clone(self.session == get_session_id()),
            **self._options,
        )

    def _update_attrs(self):
        _attrs = JSON()
        for k, v in self.kw.items():
            if callable(v) and not (
                isinstance(v, ChildrenComponent) or hasattr(v, '__render__')
            ):
                _hash = hash(v)
                _key = self.name + '___' + k + '___' + str(_hash)
                create_request(get_session_id(), _key, v)
                v = _hash
                self._options.is_in_dom = True  # need to get __id__ on callback
            _attrs[k] = v
        self.f.kw = self.kw = _attrs

    def __call__(self, *a: tuple[Callable], **kw: dict[str, object]):
        """
        @Tag()
        def custom_tag():
            pass

        cached_tag = Tag(cache=True)
        @cached_tag.update(title='test')
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

        this = self.clone()
        this.f.kw = this.kw = kw
        tag_arguments = inspect.getfullargspec(this.f._f)
        is_class_component = isinstance(this.f._f, type)

        if '_class' in kw and '_class' not in tag_arguments.args:
            kw['class'] = kw.pop('_class')
        if ('children' in kw
            and self._options.get('children_raw', False)
            and not isinstance(_children := kw.children, ChildrenComponent)
        ):
            kw['children'] = ChildrenComponent(_children)

        if len(tag_arguments.args) == is_class_component:
            this.children = this.f(**kw)
        elif 'tag' in kw:
            this.children = this.f(this.f, **kw)
        else:
            this.children = this.f(tag=this.f, **kw)

        this.children._options.parent = this

        this._update_attrs()
        this._options['init'] = False
        if is_cached:
            self._cached[cached_key] = this
        return this

    def __repr__(self):
        return str(self.name) + '(' + ', '.join(str(k) + '=' + str(v) for k, v in self.kw.items()) + ')'

    def __render__(self, children=None):
        """
        @Tag()
        class World:
            def __init__(self, **attrs):
                print('Init World')
            def __render__(self, tag):
                print('Hello World')
                return tag.__render__()
        """
        if children is None:
            children = self.children
        children = str(ChildrenComponent.escape(children, self._options.escape))
        attrs = self.kw | self.__kw
        if 'children' in attrs:
            attrs.pop('children')

        if get_attrs:
            return attrs, children

        result = '<' + self.name
        for k, v in attrs.items():
            if v is None or v is False:
                continue
            if v is True:
                result += ' ' + k
                continue
            result += ' ' + k + '="' + str(v) + '"'
        result += '>'
        if not self._options._void_tag:
            result += f'{children}</{self.name}>'

        return result

    def __str__(self):
        _hash = self.hash
        if not _hash:
            _hash = self.hash = hash(self)
        _is_in_dom = self._options.is_in_dom
        if _is_in_dom:
            set_to_dom(_hash, self)
        self._update_attrs()

        if self.f and getattr(self.f, '__render__', None) is not None:
            result = str(self.children.__render__(self))
        else:
            result = self.__render__()

        if not result:
            return ''

        result = result.replace(
            '<' + self.name,
            f'<{self.name}' + (f' pyx-id="{_hash}" pyx-dom ' if _is_in_dom else ''),
            1
        )
        return result


class MetaTag(type):
    """
    Allows to inherit Tag with updated options

    >>> cached_tag = Tag(cache=True)
    >>> class MyApp(**cached_tag.extend()): pass
    >>> assert MyApp._options.cache == True

    >>> class MyApp(**cached_tag.extend(cache=False)): pass
    >>> assert MyApp._options.cache == False
    """
    def __new__(cls, name, bases, dct, **k):
        bases = (Tag, *bases)
        self = super().__new__(cls, name, bases, dct)
        self._options = JSON(k)
        return self


class Component:
    __f__: Callable = None
    __tag__: Tag = None
    kw: JSON = JSON()
    _states: JSON = JSON()
    frame = None
    locals: dict = {}
    _state_cls: type = state

    @property
    def init(self):
        return self.__tag__.init

    def _get(self, key):
        return self._states[key]

    def _set(self, key, value):
        self._states[key] = value

    def _del(self, key):
        del self._states[key]

    def clone(self, deep=False):
        cls = type(self)

        this = cls(self.__f__)
        this.kw = self.kw
        this._state_cls = self._state_cls
        if deep:
            this._states = self._states

        return this

    def __bool__(self):
        return bool(self.__f__)

    def __new__(cls, f):
        if isinstance(f, cls):
            return f
        self = super().__new__(cls)

        if f and hasattr(f, '__globals__'):
            f.__globals__.setdefault('self', self)
        self.__f__ = f
        self.kw = JSON()
        self._states = JSON()

        return self

    def __init__(self, *a, **k):
        super().__init__()

    def __str__(self):
        return (
            '<Component ' + self.__f__.__name__ + '('
            + ', '.join(k + '=' + v for k, v in self.kw.items())
            + ')>'
        )

    def __hash__(self):
        return hash((
            self.__f__,
            self.__name__,
            self._state_cls,
        ))

    def __call__(self, *a, **k):
        f = self.__f__
        if not f or not callable(f):
            return
        return ChildrenComponent(f(*a, **k))

    def __getattr__(self, key, raw=False):
        _value = None
        if key in self._states:
            _value = self._get(key)
        elif key in dir(self.__f__):
            _value = getattr(self.__f__, key, _value)
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
            if isinstance(_exists_value, _state_cls) and _exists_value.__get_init__() == value.__get__():
                return
            else:
                return self._set(key, value)
        else:
            if isinstance(_exists_value, _state_cls):
                return _exists_value.__set__(value)
            else:
                return super().__setattr__(key, value)

    def __delattr__(self, key):
        if key in dir(self):
            return super().__delattr__(key)

        _exists_value: Union[state, object] = self.__getattr__(key, raw=True)

        if isinstance(_exists_value, self._state_cls):
            return _exists_value.__del__()
        else:
            return super().__delattr__(key)


cached_tag = Tag(cache=True)

