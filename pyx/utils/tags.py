from .core import camel_or_snake_to_kebab_case


def parse_tag_name(name: str) -> str:
    """
    parsing name of tag (function or class) to html-compatible
    >>> def __pyx__(): ...  # <pyx></pyx>
    >>> class __html__: ...  # <html></html>
    >>> def myTagName(): ...  # <my-tag-name/>
    >>> def very_cool_name(): ...  # <very-cool-name/>
    >>> def _doNotRepeat_this_please(): ...  # <do-not-repeat-this-please/>
    """
    name = name.strip('_')

    name = camel_or_snake_to_kebab_case(name)

    return name
