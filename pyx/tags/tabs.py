from .all import li, ul, div
from ..utils import state, ChildrenComponent
from ..main import cached_tag
from .default import DEFAULT_TAG


@cached_tag
def tab(*, name, children, on_click=None):
    return li(children=name)


@DEFAULT_TAG.update(is_in_dom=True)
def tabs(tag, selected=None, children=()):
    if selected is None and children:
        selected = children[0].kw.name
    tag.selected = state(selected)
    print(tag.selected)

    for child in children:
        child.kw.active = tag.selected == child.kw.name
        child.kw.on_click = lambda tab=child: set_selected(tab)

    def set_selected(tab):
        tag.selected = tab.kw.name
        return 'selected: ' + str(tag.selected)

    return div(children=[
        ul(children=children),
        div(children=ChildrenComponent([
            child.kw.get('children')
            for child in children
            if not isinstance(child, str) and child.kw.active
        ]))
    ])
