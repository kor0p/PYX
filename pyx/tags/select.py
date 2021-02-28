from typing import Union

from ..utils import JSON
from ..main import cached_tag, Component


class SelectItem(JSON):
    label: str
    value: str


class SelectItems:
    @staticmethod
    def _get_data(*args, **kwargs):
        if kwargs:
            return kwargs
        if len(args) != 1:
            return
        data = args[0]
        if isinstance(data, dict):
            return data
        if hasattr(data, '__get__'):
            _data = data.__get__()
            if isinstance(_data, dict):
                return _data

    def __new__(cls, *args, **kwargs) -> list:
        data = cls._get_data(*args, **kwargs)
        if data:
            if 'label' not in data or 'value' not in data:
                return [SelectItem(label=v, value=k) for k, v in data.items()]
            return list(map(SelectItem, data))
        if args:
            return list(map(SelectItem, args))
        return [SelectItem(*args, **kwargs)]


@cached_tag
def option(*, label, **attrs):
    return label


@cached_tag
def select(tag: Component, **k):
    items = SelectItems(tag.kw.pop('items'))
    return [
        option(
            **item,
            selected=(
                tag.kw.value == item.value or
                tag.kw.value == item.label
            )
        )
        for item in items
    ]