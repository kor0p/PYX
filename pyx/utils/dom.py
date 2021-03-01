from .rand import get_random_name
from .app import get_cookie

__sessions__ = {}

__PYX_ID__ = f'__pyx_id_{get_random_name()}__'


def get_dom():
    dom = __sessions__.get(get_cookie(__PYX_ID__))
    if dom is None:
        raise ConnectionError('cannot get session')
    return dom


def set_dom(_id, dom=None):
    __sessions__[_id] = dom or {}


def get_from_dom(tag):
    if isinstance(tag, str):
        _id = tag
    else:
        _id = str(hash(tag))
    return get_dom().get(_id)


def set_to_dom(key_or_value, value=None):
    dom = get_dom()
    if value:
        dom[str(key_or_value)] = value
    else:
        dom[str(hash(key_or_value))] = key_or_value
