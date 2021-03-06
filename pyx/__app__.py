from typing import Union
from datetime import datetime

from pyx.tags import render_error, __html__
from pyx.utils.dom import set_dom, get_from_dom, __PYX_ID__, get_session_id, del_dom
from pyx.utils.app import create_app, get_cookies, set_cookie, make_response, handle_requests
from pyx.utils import get_random_name, join
from pyx.main import Tag, PYXModule


__APP__ = create_app(__name__)
__APP__.__PYX_ID__ = __PYX_ID__
__APP__._get_session_id = get_session_id


def render(body: Union[Tag, PYXModule]):
    cookies = get_cookies()
    _ids_to_remove = [name for name in cookies.keys() if '__pyx_id' in name and __PYX_ID__ != name]
    exists = get_session_id() is not None
    pyx_id = None
    if not exists:
        pyx_id = get_random_name()
        set_cookie(__PYX_ID__, pyx_id)
        set_dom(pyx_id)

    if not isinstance(body, Tag):
        body = body.__pyx__()
    result = str(__html__(children=body))
    if exists and not _ids_to_remove:
        return result

    response = make_response(result)
    for _id in _ids_to_remove:
        del_dom(_id)
        set_cookie(_id, '', response, expires=0)
    if not exists:
        set_cookie(__PYX_ID__, pyx_id, response, expires=datetime.strptime('2100', '%Y'))
    return response


handle_requests(
    __APP__,
    '/pyx',
    lambda r, kw: render_error(traceback=r, session=__PYX_ID__, **kw),
    lambda _id: get_from_dom(_id)()
)


def run_app(*a, **k):
    return __APP__.run(*a, **(k or dict(debug=True)))

# TODO: add FastAPI app
