import re
from .core import join, camel_or_snake_to_kebab_case


def dict_of_properties_to_css(properties):
    for prop, value in properties.items():
        if not isinstance(prop, (tuple, set)):
            prop = (prop,)
        result = ''
        for _property in prop:
            _property = camel_or_snake_to_kebab_case(_property)

            # if '&' in _property:
            #     _property = re.sub('&', parent, _property)
            result += '    ' + _property
            if isinstance(value, (list, tuple)):  # handle raw css
                result += ' ' + join(_property + ' ', value)
            else:
                result += f': {value};'
        yield result


def dict_of_parents_to_css(children, parent):
    for child, value in children.items():
        if isinstance(child, (tuple, set)):
            child = join(',', child)
        if '&' in child:
            child = re.sub('&', parent, child)
        else:
            child = parent + ' ' + child
        for inner in dict_to_css(value, child):
            if child.startswith('@') and not parent:
                inner = f' {{ {inner.strip()} }}'
            yield inner


def dict_to_css(selectors: dict, parent: str = ''):
    """
    parses nested dict to css

    dict(
        div=dict(
            color='red',
            backgroundColor='blue',
            p={
                'font-size': '20px',
                '&.class': dict(
                    font_size='30px',
                )
            }
        )
    )

    to

    div {
        color: red;
        background-color: blue;
    }
    div p {
        font-size: 20px;
    }
    div p.class {
        font-size: 30px;
    }


    """
    children = {}
    properties = {}

    for prop, value in selectors.items():
        if isinstance(value, dict):
            children[prop] = value
        else:
            properties[prop] = value

    if properties:
        yield parent
        yield ' {'
        yield from dict_of_properties_to_css(properties)
        yield '}'

    yield from dict_of_parents_to_css(children, parent)


class css:
    """
    style(
        css(
            div=dict(
                color='red',
            ),
            p={
                'font-size': '20px',
            }
        )
    )

    """

    def __init__(self, _dict=None, /, **selectors):
        if _dict is not None:
            if not isinstance(_dict, dict):
                raise SyntaxError('Argument must be dictionary', _dict)
            if selectors:
                raise SyntaxError("Wrong arguments: don't use both args and kwargs", _dict, selectors)
            selectors = _dict
        self._selectors = selectors

        self.value = join('\n', list(dict_to_css(selectors)))

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self._selectors)
