import re

from ..main import cached_tag, Component, Tag


DEFAULT_HEAD = '''
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="/static/js/pyx.js"></script>
<script type="text/typescript" src="/static/js/test.ts"></script>
<link type="text/css" rel="stylesheet" href="/static/css/pyx.css"/>'''

DEFAULT_BODY = '''
<error>
    <render_error/>
</error>
'''

DEFAULT_TAG = cached_tag.update(is_in_dom=False)(None)


@DEFAULT_TAG.update(name='input')
def inp(**k):
    return


@Tag
def python(tag, **k):
    __locals = {}
    __globals = globals().copy()
    if '_locals' in k:
        __globals.update(tag.kw.pop('_locals'))
    # print(__locals)
    if 'src' in k:
        with open(k['src'], 'r') as src:
            code = '\n'.join('    ' + line for line in src.readlines())
    else:
        children = str(k.get('children', ''))
        tabs = re.search('\n?(?P<spaces> *)', children).group('spaces')
        code = re.sub('^' + tabs, '    ', children, flags=re.MULTILINE)
    exec(f'''
def __python__():
{code}
''', __globals, __locals)
    return __locals['__python__']()


@DEFAULT_TAG
def render_error(*a, **k):
    return f'ERROR:\n  args: {a}\n  kwargs: {k}'


@DEFAULT_TAG
class __fragment__:
    def __init__(self, **k):
        pass

    def __render__(tag: Tag):
        return tag.k.children


@cached_tag.update(name='head')
def __head__(*, children=''):
    return DEFAULT_HEAD + str(children)


@cached_tag.update(name='body')
def __body__(*, children=''):
    return str(children) + DEFAULT_BODY


@cached_tag.update(name='html')
def __html__(*, head='', children=''):
    return __fragment__(children=[
        __head__(children=head),
        __body__(children=children),
    ])
