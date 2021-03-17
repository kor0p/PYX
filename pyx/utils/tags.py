import regex


def parse_tag_name(name: str) -> str:
    """
    parsing name of tag (function or class) to html-compitible
    >>> def __pyx__(): ...  # <pyx></pyx>
    >>> class __html__: ...  # <html></html>
    >>> def myTagName(): ...  # <my-tag-name/>
    >>> def very_cool_name(): ...  # <very-cool-name/>
    >>> def _doNotRepeat_this_please(): ...  # <do-not-repeat-this-please/>
    """
    name = name.strip('_')

    name = regex.sub('_', '-', name)
    name = regex.sub(
        r'(\p{Lu})',  # this matches all uppercase unicode symbols
        lambda m: '-' + m.group(1).lower(),
        name
    )

    return name
