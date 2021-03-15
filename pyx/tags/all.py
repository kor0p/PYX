from .default import DEFAULT_TAG, VOID_TAG
from ..utils.children import ChildType


@DEFAULT_TAG
def a(href=None, *_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def abbr(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def acronym(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def address(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def applet(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def area(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def article(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def aside(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def audio(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def b(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def base(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def basefont(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def bdi(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def bdo(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def big(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def blockquote(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def br(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(is_in_dom=True)
def button(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def canvas(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def caption(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def center(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def cite(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def code(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def col(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def colgroup(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def data(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def datalist(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dd(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(title='del')
def _del(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def details(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dfn(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dialog(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dir(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def div(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dl(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def dt(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def em(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def embed(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def fieldset(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def figcaption(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def figure(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def font(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def footer(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def form(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def frame(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def frameset(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h1(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h2(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h3(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h4(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h5(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def h6(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def header(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def hr(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def i(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def iframe(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def img(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG.update(title='input')
def _input(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ins(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def kbd(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def label(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def legend(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def li(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def link(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def main(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(title='map')
def _map(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def mark(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def meta(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def meter(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def nav(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def noframes(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def noscript(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG.update(title='object')
def _object(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ol(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def optgroup(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def option(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def output(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def p(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def param(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def picture(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def pre(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def progress(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def q(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def rp(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def rt(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ruby(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def s(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def samp(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def section(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def select(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def small(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def source(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def span(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def strike(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def strong(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def sub(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def summary(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def sup(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def svg(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def table(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tbody(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def td(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def template(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def textarea(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tfoot(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def th(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def thead(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def time(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def title(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tr(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def track(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def tt(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def u(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def ul(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def var(*_, children: ChildType = '') -> ChildType:
    return children


@DEFAULT_TAG
def video(*_, children: ChildType = '') -> ChildType:
    return children


@VOID_TAG
def wbr(*_, children: ChildType = '') -> ChildType:
    return children
