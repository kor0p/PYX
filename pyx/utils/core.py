import re
import sys
import regex
from typing import Callable
from operator import attrgetter


get_ = attrgetter


def is_class(cls):
    return isinstance(cls, type)


def camel_or_snake_to_kebab_case(string: str):
    """
    parsing name of tag to html-compatible or name of property to css-compatible
    >>> def __pyx__(): ...  # <pyx></pyx>
    >>> def myTagName(): ...  # <my-tag-name/>
    >>> css(font_size='20px')  # font-size: 20px
    >>> css(backgroundColor='red')  # background-color: red
    """
    string = regex.sub('_', '-', string)
    string = regex.sub(
        r'(\p{Lu})',  # this matches all uppercase unicode symbols
        lambda m: '-' + m.group(1).lower(),
        string,
    )
    return string


def remove_spaces_after_newline(string, replace_with=''):
    tabs = re.search('\n?(?P<spaces> *)', string).group('spaces')
    return re.sub('^' + tabs, replace_with, string, flags=re.MULTILINE)


class classproperty:
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class staticproperty:
    """
    @property for @staticmethod
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, *a):
        return self.fget()


def join(sep, iterable, mapper: Callable[[object], str] = str, except_values=(None,)):
    return sep.join(map(lambda v: '' if v in except_values else mapper(v), iterable))


def escape(s, quote=True):
    """
    # forked from html.escape
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


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
