from .all import li, ul, div
from ..utils import state
from ..main import cached_tag


@cached_tag
def tab(*, name, on_click):
    # if active:
    return li(children=name)


@cached_tag
def tabs(tag, selected=0, children=()):
    tag.selected = state(selected)

    for index, child in enumerate(children):
        child.kw.active = tag.selected == child.name
        child.kw.on_click = lambda i=index: set_selected(i)

    def set_selected(index):
        tag.selected = index
        return 'selected: ' + str(tag.selected)

    return div(children=[
        ul(children=children),
        div(children=children and children[tag.selected].get('content'))
    ])
