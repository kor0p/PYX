from ..main import Tag
from .default import DEFAULT_TAG
from ..utils import __extra__


class script(Tag, **DEFAULT_TAG.extend):
    def __init__(self, children='', scoped=True, src='', **kwargs):
        self.scoped = scoped
        self.children = children
        self.src = src
        self.kwargs = kwargs

    def __render__(self):
        if not self.scoped:
            __extra__.js.append(str(self['children':]))
            return ''
        return super().__render__()
