import re

from .default import cached_tag, __extra__
from ..utils.rand import get_random_name
from .all import link

try:
    import sass
except ImportError:
    sass = None  # if in projects not using scss/sass


_pyx_style_attr = 'pyx-style'


class style(**cached_tag.extend):
    def __init__(self, *, src=None, **kwargs):
        self.src = src
        self.kwargs = kwargs
        if self.src is not None:
            return

        if kwargs.get('lang') in ('scss', 'sass'):
            self.kwargs['children'] = sass.compile(
                string=kwargs.get('children'),
                **kwargs.get('sass_options', {})
            )

    def _scope_style(self, styles, *, style_name=None):
        """https://stackoverflow.com/a/32134836/8851903"""
        if not style_name:
            style_name = get_random_name()
        scoped_data = f'{_pyx_style_attr}="{style_name}"'
        css_rules = re.findall(r'[^{]+{[^}]*}', styles, re.MULTILINE)
        return (
            (_pyx_style_attr, style_name),
            '\n'.join(
                ','.join(
                    f'[{scoped_data}] {item}'
                    for item in rule.strip().split(',')
                )
                for rule in css_rules
            ) + '\n'
        )

    def __render__(self):
        if self.src:
            _link = str(link(rel='stylesheet', type='text/css', href=self.src, **self.kwargs))
            if not self.kwargs.get('head', True):
                self.kwargs.pop('head')
                return _link
            __extra__.head.append(_link)
            return

        children = self.kwargs.get('children')

        if self.kwargs.get('scoped'):
            if style_name := self.parent.kw.get(_pyx_style_attr):
                _, children = self._scope_style(children, style_name=style_name)
            else:
                (attr, style_name), children = self._scope_style(children)
                self.parent[_pyx_style_attr] = style_name

        if self.kwargs.get('head', False):
            __extra__.css.append(children)
        else:
            return super().__render__(children)
