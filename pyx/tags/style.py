import re
import os

from .default import cached_tag, __extra__
from ..main import Tag
from ..utils.core import remove_spaces_after_newline
from ..utils.rand import get_random_name
from .all import link

try:
    import sass
except ImportError:
    sass = None  # if in projects not using scss/sass


class style(**cached_tag.extend):
    _pyx_style_attr = 'pyx-style'

    def __init__(self, children='', src=None, scoped=False, **kwargs):
        children = str(children)
        kwargs.setdefault('lang', os.environ.get('__PYX_STYLE_LANG__'))

        kwargs['children'] = remove_spaces_after_newline(children)

        self['scoped'] = scoped
        self.src = src
        self.kwargs = kwargs
        if self.src is not None:
            return

        if (lang := kwargs.get('lang')) in ('scss', 'sass'):
            self.kwargs['children'] = sass.compile(
                string=kwargs['children'],
                indented=lang == 'sass',
                **kwargs.get('sass_options', {}),
            )

    def _scope_style(self, styles, *, style_name=None):
        """https://stackoverflow.com/a/32134836/8851903"""
        if not style_name:
            style_name = get_random_name()
        scoped_data = f'[{self._pyx_style_attr}="{style_name}"]'
        css_rules = re.findall(r'[^{]+{[^}]*}', styles, re.MULTILINE)
        return (
            (self._pyx_style_attr, style_name),
            '\n'.join(
                ',\n'.join(f'{scoped_data} {item.strip()}' for item in rule.strip().split(',')) for rule in css_rules
            )
            + '\n',
        )

    def __render__(self):
        if self.src:
            _link = str(link(rel='stylesheet', type='text/css', href=self.src, **self.kwargs))
            if not self.kwargs.get('head', True):
                self.kwargs.pop('head')
                return _link
            __extra__.head.append(_link)
            return

        children = self.kwargs['children']

        if self['scoped']:
            if style_name := self.parent[self._pyx_style_attr]:
                _, children = self._scope_style(children, style_name=style_name)
            else:
                (attr, style_name), children = self._scope_style(children)
            self.parent[self._pyx_style_attr] = style_name

        if self.kwargs.get('head', False):
            __extra__.css.append(children)
        else:
            return super().__render__(children)
