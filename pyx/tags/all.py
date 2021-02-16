from .default import DEFAULT_TAG


@DEFAULT_TAG
def a(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def abbr(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def acronym(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def address(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def area(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def b(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def base(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def bdo(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def big(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def blockquote(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def body(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def br(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def button(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def caption(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def cite(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def code(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def col(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def colgroup(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def dd(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG.update(name='del')
def _del(**k):
    return str(k.get('children', ''))
locals()['del'] = _del


@DEFAULT_TAG
def dfn(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def div(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def dl(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def DOCTYPE(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def dt(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def em(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def fieldset(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def form(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def h1(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def h2(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def h3(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def h4(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def h5(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def h6(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def head(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def html(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def hr(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def i(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def img(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def input(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def ins(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def kbd(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def label(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def legend(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def li(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def link(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def map(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def meta(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def noscript(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def object(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def ol(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def optgroup(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def option(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def p(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def param(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def pre(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def q(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def samp(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def script(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def select(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def small(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def span(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def strong(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def style(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def sub(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def sup(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def table(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def tbody(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def td(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def textarea(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def tfoot(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def th(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def thead(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def title(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def tr(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def tt(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def ul(**k):
    return str(k.get('children', ''))


@DEFAULT_TAG
def var(**k):
    return str(k.get('children', ''))
