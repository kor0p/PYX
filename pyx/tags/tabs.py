from .all import li, ul, div, a
from ..utils.state import state
from ..utils.children import ChildrenComponent
from .default import DEFAULT_TAG
from .script import script


@DEFAULT_TAG.update(is_in_dom=True)
def tab(*, name, children, active=None, on_click=None, url=None, href=None):
    return li(a(name, href=href) if href else name)


@DEFAULT_TAG.update(is_in_dom=True, escape=False)
def tabs(tag, selected=None, children=(), _class=''):
    if selected is None and children:
        selected = children[0]['name']
    tag.selected = state(selected)

    for child in children:
        child['active'] = tag.selected == child['name']
        child['on_click'] = lambda t=child: set_selected(t)
        if callable(children_kwarg := child['children']):
            child['children'] = children_kwarg()

    def set_selected(t):
        tag.selected = t['name']
        return 'selected: ' + str(tag.selected)

    return [
        ul(children),
        div(
            _class=_class,
            children=ChildrenComponent(
                [child['children'] for child in children if not isinstance(child, str) and child['active']]
            ),
        ),
        script(
            r'''
            const activeTab = $('tab[active]')
            const name = activeTab.attr('url') || activeTab.attr('name')
            const pathname_trailing_slash = window.location.pathname.replace(/\/$/g, '')
            window.history.pushState(name, name, pathname_trailing_slash + activeTab.attr('url'))
            function handleToggleTab() {
                $('tab').off('click::after').on('click::after', (e, { self }) => {
                    if (self.attr('active')) {
                        console.log(self)
                    }
                    const name = self.attr('name')
                    window.history.pushState(name, name, pathname_trailing_slash + self.attr('url'))
                    handleToggleTab() // after reload old jQuery not working
                })
            }
            handleToggleTab()
        '''
        ),
    ]
