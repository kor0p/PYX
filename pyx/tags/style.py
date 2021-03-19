import re

from .default import cached_tag, __extra__
from ..utils.rand import get_random_name
from .all import link


class style(**cached_tag.extend):
    def __init__(self, *, src=None, **kwargs):
        self.src = src
        self.kwargs = kwargs
        if self.src is not None:
            return
        if kwargs.get('scoped'):
            scoped, children = self._scope_style(kwargs.get('children'))
            kwargs.update(dict(scoped=scoped, children=children))

    def _scope_style(self, styles):
        """https://stackoverflow.com/a/32134836/8851903"""
        style_name = get_random_name()
        scoped_data = f'pyx-style="{style_name}"'
        css_rules = re.findall(r'[^{]+{[^}]*}', styles, re.MULTILINE)
        return (
            ('pyx-style', style_name),
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
        attr, style_name = self.kwargs.get('scoped')
        self.parent.kw[attr] = style_name
        if self.kwargs.get('head', False):
            __extra__.css.append(self.kwargs.get('children'))
        else:
            return super().__render__(self.kwargs.get('children'))
