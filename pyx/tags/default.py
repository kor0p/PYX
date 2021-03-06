from ..utils import __extra__
from ..utils.core import remove_spaces_after_newline
from ..utils.children import ChildrenComponent
from ..main import cached_tag, Tag


DEFAULT_HEAD = '''
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="/pyx/static/js/pyx.js"></script>
<script type="text/typescript" src="/pyx/static/js/test.ts"></script>
<link type="text/css" rel="stylesheet" href="/pyx/static/css/pyx.css"/>
<style>
    {extra_css}
</style>
{extra_head}
'''

__extra__.css = ChildrenComponent()
__extra__.head = ChildrenComponent()

DEFAULT_BODY = '''
<error>
    <render_error/>
</error>
<script>
    {extra_js}
</script>
{extra_body}
'''

__extra__.js = ChildrenComponent()
__extra__.body = ChildrenComponent()

DEFAULT_TAG: Tag = cached_tag.update(is_in_dom=False)
MAIN_TAG: Tag = cached_tag.update(escape=False)
VOID_TAG: Tag = DEFAULT_TAG.update(_void_tag=True)


@Tag
def python(tag: Tag, **k):
    """
    <python>
        # this code will be compiled as a function with current locals
        # and the result of function will be returned to html
        print("Hey, python tag!")
        return 1 + 1
    </python>

    # in console
    Hey, python tag!
    # in browser
    <python>
        2
    </python>
    """
    __locals = locals()
    __globals = globals()
    if '_locals' in k:
        __locals = tag['_locals':]
    if '_globals' in k:
        __globals = tag['_globals':]
    if 'src' in k:
        with open(k['src'], 'r') as src:
            code = '\n'.join('    ' + line for line in src.readlines())
    else:
        children = str(k.get('children', ''))
        code = remove_spaces_after_newline(children, '    ')
    exec(
        f'''
def __python__():
{code}
''',
        __globals,
        __locals,
    )
    return __locals['__python__']()


@DEFAULT_TAG
def render_error(traceback: str, **k) -> str:
    children = f'ERROR:\n  traceback: {traceback}\n  kwargs: {k}'
    print(children)
    return children


class __fragment__(**DEFAULT_TAG.extend):
    def __init__(self, *, children=''):
        self.children = children

    def __render__(self, tag):
        return str(self.children)


@MAIN_TAG
def __head__(*, children=''):
    return (
        DEFAULT_HEAD.format(
            extra_css=__extra__.css,
            extra_head=__extra__.head,
        )
        + children
    )


@MAIN_TAG
def __body__(*, children=''):
    return children + DEFAULT_BODY.format(
        extra_js=__extra__.js,
        extra_body=__extra__.body,
    )


@MAIN_TAG
def __html__(*, head='', children=''):
    __extra__.css = ChildrenComponent()
    __extra__.head = ChildrenComponent()
    __extra__.js = ChildrenComponent()
    __extra__.body = ChildrenComponent()
    _body = __body__(str(children))
    _head = __head__(str(head))
    return [_head, _body]
