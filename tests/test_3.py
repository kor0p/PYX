
from pyx import *  # importing all: tag, default tags (div, select, tabs, etc.), ...
from pyx import (  # importing extra data for pyx render
    __fragment__,
)
from pyx import Tag, state, select, p  # not necessary, really

@cached_tag.update(title='div')
def func(tag):
    tag.selected = state(1)
    items = {0: 'first', 1: 'second', 2: 'third'}
    def _select(value):
        tag.selected = int(value)
    return __fragment__(**{"children": [p(**{"children": [f"""Key: {tag.selected}"""]}), style(**{
        "src": "/pyx/static/css/pyx.css",
        }), p(**{
        "@click.right:prevent": lambda: 'GOT IT',
        "children": [f"""Value: {items[tag.selected]}"""]}), select(**{
        "items": items,
        "@change:prevent": _select,
        "value": tag.selected,
        })]})


__pyx__ = func

tags_set = {'p', '__pyx__', '__fragment__', 'select'}


l = locals()
for tag_name in tags_set:
    if _tag := l.get(tag_name):
        l[tag_name] = cached_tag(_tag)
    else:
        l[tag_name] = Tag(name=tag_name)(div)
