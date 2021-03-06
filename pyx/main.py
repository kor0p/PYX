import inspect
import keyword
from typing import Union, Optional, Callable, TypeVar, Any
from types import ModuleType

from .utils.app import create_request, get_request
from .utils.children import ChildrenComponent
from .utils.core import get_, is_class
from .utils.dom import set_to_dom, get_session_id
from .utils.tags import parse_tag_name
from .utils.JSON import JSON
from .utils.state import state, __wrapper__

T = TypeVar('T', bound='Tag')
C = TypeVar('C', bound='Component')


class ClassComponent:
    __render__: Callable


class PYXModule(ModuleType):
    __pyx__: Callable


class Options(JSON):
    title: str
    cache: bool
    is_in_dom: bool
    children_raw: bool
    init: bool
    escape: bool

    _void_tag: bool

    # runtime config
    parent: T
    changed: bool

    def __init__(self, *a, **k):
        if a:
            super().__init__(*a, **k)
            return
        k.setdefault('cache', False)
        k.setdefault('is_in_dom', True)
        k.setdefault('children_raw', False)
        k.setdefault('init', True)
        k.setdefault('escape', True)

        k.setdefault('_void_tag', False)
        super().__init__(**k)


class Tag:
    f: Optional[C] = None
    kw: JSON = JSON()
    __kw: JSON = JSON()
    hash: Optional[int] = None
    session: Optional[str] = None
    parent: Optional[T] = None
    children: ChildrenComponent[Union[str, ClassComponent]] = ''
    _cached: dict = {}
    _underscore_attributes = ['_' + attr for attr in keyword.kwlist]  # async, class, for, etc.
    _tag_argspec: Optional[inspect.FullArgSpec] = None
    _options: Options = Options()

    def __len__(self):
        return 0

    def __bool__(self):
        return bool(self.f)

    @property
    def extend(self) -> dict:
        return dict(metaclass=MetaTag, _opts=self._options)

    def __add__(self, other):
        return ChildrenComponent([self, other])

    @property
    def _is_class(self):
        return bool(self.f) and is_class(self.f.__f__)

    @property
    def _is_class_component(self):
        return self._is_class and issubclass(self.f.__f__, Tag)

    @property
    def init(self):
        """
        def pyx(tag):
            if tag.init:
                print('inited')
            return ''
        """
        return self._options.init

    @property
    def parent(self) -> T:
        return self._options.parent

    @property
    def name(self) -> str:
        return self._options.title or 'div'

    @name.setter
    def name(self, name: str) -> None:
        self._options.title = name

    def update(self, **k) -> T:
        return type(self)(self.f.__f__, **(self._options | k))

    def __getitem__(self, key: Union[str, slice]) -> Any:
        """
        get attribute of Tag
        if there is a colon in the end,
        result will be be popped from attr list

        >>> ...
        >>> @cached_tag
        ... def select(tag: Component):
        ...     items = SelectItems(tag['items':])  # this removes [items] attribute
        ...     return [
        ...         option(
        ...             **item,
        ...                 selected=tag['value'] in (item.value, item.label)
        ...             )   #  tag['value'] just return [value] attribute
        ...         for item in items
        ...     ]
        """
        fn = get_('get')

        if isinstance(key, slice):
            key = key.start
            fn = get_('pop')

        if key in self.kw:
            return fn(self.kw)(key)

        return fn(self.__kw)(key)

    def __setitem__(self, key, value):
        if key in self.kw or (self._tag_argspec and self._tag_argspec.varkw):
            self.kw[key] = value
            return

        self.__kw[key] = value

    def __new__(cls, f=None, **k):
        if isinstance(f, cls):
            return f
        self = super().__new__(cls)

        if f is not None and (not callable(f) or isinstance(f, ChildrenComponent)):
            self.__init__(children=f, **k)
            return self
        self.__kw = JSON()
        if f:
            k.setdefault('title', f.__name__)
            k['title'] = parse_tag_name(k['title'])
            self._tag_argspec = inspect.getfullargspec(f)

        self._options = Options(**(self._options | k))

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

    def _get_cached_key(self, kwargs: dict):
        return (
            self.name,
            hash(self.f),
            tuple(sorted((a, str(b)) for a, b in kwargs.items())),
        )

    def clone(self, *, deep=False):
        cls = type(self)
        this = cls(
            self.f.clone(self.session == get_session_id()),
            **self._options,
        )
        if deep:
            this._Tag__kw = self.__kw.copy()
        return this

    def _handle_callable_attrs(self, k, v):
        _key = self.name + '___' + k + '___' + str(hash(self))
        session = get_session_id()
        if r := get_request(session, _key):
            return hash(r)
        create_request(session, _key, v)
        self._options.is_in_dom = True  # need to get __id__ on callback
        return hash(v)

    def _update_attrs(self):
        _attrs = JSON()
        for k, v in self.kw.items():
            if callable(v) and not (isinstance(v, ChildrenComponent) or hasattr(v, '__render__')):
                v = self._handle_callable_attrs(k, v)
            _attrs[k] = v
        self.kw = _attrs

        _attrs = JSON()
        for k, v in self.__kw.items():
            if callable(v):
                v = self._handle_callable_attrs(k, v)
            _attrs[k] = v
        self.__kw = _attrs

    def __call__(
        self,
        decorator_or_children: Union[Callable, str] = None,
        *rest_children,
        **kw: dict[str, Any],
    ):
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
        if decorator_or_children:
            if callable(decorator_or_children) and not isinstance(decorator_or_children, ChildrenComponent):
                return type(self)(decorator_or_children, **self._options)
            else:
                kw['children'] = [decorator_or_children, *rest_children] if rest_children else decorator_or_children
        is_cached = self._options.cache

        this = None
        cached_key = None
        if is_cached:
            cached_key = self._get_cached_key(self.kw | kw)
            if cached := self._cached.get(cached_key):
                if cached._options.changed:
                    this = cached
                else:
                    return cached

        if this is None:
            this = self.clone(deep=True)
        this.kw = JSON(self.kw | kw)
        tag_argspec = self._tag_argspec
        if not tag_argspec:
            tag_argspec = self._tag_argspec = inspect.getfullargspec(this.f.__f__)
        _is_class = self._is_class
        args_names = [*tag_argspec.args, *tag_argspec.kwonlyargs]

        if not tag_argspec.varkw:
            for attr_name in kw.copy().keys():
                if attr_name not in args_names and '_' + attr_name not in self._underscore_attributes:
                    this.__kw[attr_name.strip('_')] = kw.pop(attr_name)
                    this.kw.pop(attr_name)

        for underscored in self._underscore_attributes:
            if underscored in kw and underscored not in tag_argspec.args:
                this.kw[underscored[1:]] = this[underscored:]

        if 'children' in kw and (self._options.children_raw or not isinstance(kw['children'], ChildrenComponent)):
            this.kw['children'] = ChildrenComponent(kw['children'])

        if len(tag_argspec.args) == 0 or _is_class:
            this.children = this.f(**this.kw)
        elif 'tag' in kw:
            this.children = this.f(this.f, **this.kw)
        else:
            this.children = this.f(tag=this.f, **this.kw)

        this.children._options.parent = this

        this._update_attrs()
        this._options.init = False
        this._options.changed = False
        if is_cached and not self.init:
            self._cached[cached_key] = this
        return this

    def __repr__(self):
        return str(self.name) + '(' + ', '.join(str(k) + '=' + str(v) for k, v in self.kw.items()) + ')'

    def __render__(self, children=None, *, get_attrs=False):
        """
        class World(**Tag.extend):
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

        if self.f and self._is_class_component:
            result = str(self.children.__render__())
        elif self.f and callable(getattr(self.f, '__render__', None)):
            result = str(self.children.__render__(self))
        else:
            result = self.__render__()

        if not result:
            return ''

        name = self.name
        return result.replace('<' + name, f'<{name}' + (f' pyx-id="{_hash}" pyx-dom ' if _is_in_dom else ''), 1)


class MetaTag(type):
    """
    Allows to inherit Tag with updated options

    >>> cached_tag = Tag(cache=True)
    >>> class MyApp(**cached_tag.extend): pass
    >>> assert MyApp._options.cache == True

    >>> class MyApp(Tag, **cached_tag.extend, cache=False): pass  # you can extend Tag or MyApp to IDE can work properly
    >>> assert MyApp._options.cache == False
    """

    def __new__(mcs, name, bases, dct, **kwargs):
        if bases and not issubclass(bases[0], Tag):
            bases = (Tag, *bases)
        self = super().__new__(mcs, name, bases, dct)

        if 'title' not in kwargs:
            kwargs['title'] = name
        parent_options = kwargs.pop('_opts')
        self._options = Options(parent_options | kwargs)
        self.__bool__ = lambda _self: True

        return self


class Component:
    __f__: Callable = None
    __tag__: Tag = None
    _states: JSON = JSON()
    frame = None
    locals: dict = {}
    _state_cls: type(state) = state

    @property
    def init(self):
        return self.__tag__.init

    @__wrapper__
    def __getitem__(self, key):
        return self.__tag__[key]

    @__wrapper__
    def __setitem__(self, key, value):
        self.__tag__[key] = value

    def _get(self, key):
        return self._states[key]

    def _set(self, key, value):
        self._states[key] = value

    def _del(self, key):
        del self._states[key]

    def clone(self, deep=False):
        cls = type(self)

        this = cls(self.__f__)
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
        self._states = JSON()

        return self

    def __init__(self, *a, **k):
        super().__init__()

    def __str__(self):
        return '<Component ' + self.__f__.__name__ + '(' + ', '.join(k + '=' + v for k, v in self.kw.items()) + ')>'

    def __hash__(self):
        return hash((self.__f__, self.__name__, self._state_cls))

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
                if not value._name:
                    value._name = key
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


# cached_tag = Tag(cache=True)
cached_tag = Tag(cache=False)
