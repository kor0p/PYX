from .default import DEFAULT_TAG, VOID_TAG


@DEFAULT_TAG
def a(href=None, *, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def abbr(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def acronym(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def address(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def applet(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def area(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def article(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def aside(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def audio(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def b(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def base(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def basefont(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def bdi(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def bdo(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def big(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def blockquote(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def br(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG.update(is_in_dom=True)
def button(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def canvas(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def caption(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def center(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def cite(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def code(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def col(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def colgroup(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def data(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def datalist(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def dd(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG.update(title='del')
def _del(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def details(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def dfn(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def dialog(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def dir(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def div(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def dl(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def dt(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def em(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def embed(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def fieldset(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def figcaption(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def figure(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def font(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def footer(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def form(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def frame(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def frameset(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def h1(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def h2(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def h3(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def h4(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def h5(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def h6(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def header(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def hr(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def i(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def iframe(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def img(*, children: str = '') -> str:
    return str(children)


@VOID_TAG.update(title='input')
def _input(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def ins(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def kbd(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def label(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def legend(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def li(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def link(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def main(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG.update(title='map')
def _map(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def mark(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def meta(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def meter(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def nav(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def noframes(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def noscript(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG.update(title='object')
def _object(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def ol(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def optgroup(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def option(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def output(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def p(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def param(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def picture(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def pre(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def progress(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def q(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def rp(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def rt(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def ruby(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def s(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def samp(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def section(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def select(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def small(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def source(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def span(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def strike(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def strong(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def sub(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def summary(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def sup(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def svg(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def table(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def tbody(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def td(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def template(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def textarea(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def tfoot(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def th(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def thead(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def time(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def title(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def tr(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def track(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def tt(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def u(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def ul(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def var(*, children: str = '') -> str:
    return str(children)


@DEFAULT_TAG
def video(*, children: str = '') -> str:
    return str(children)


@VOID_TAG
def wbr(*, children: str = '') -> str:
    return str(children)
