from pyx.tags import render_error, __html__
from pyx.utils.dom import set_dom, get_from_dom, __PYX_ID__
from pyx.utils.app import create_app, get_cookies, get_cookie, set_cookie, make_response, handle_requests
from pyx.utils import get_random_name, join
from pyx.main import Tag


__APP__ = create_app(__name__)
__APP__.__PYX_ID__ = __PYX_ID__


def render(body: Tag):
    cookies = get_cookies()
    _ids_to_remove = []
    if __PYX_ID__ in join(' ', cookies.keys()):
        _ids_to_remove = [name for name in cookies.keys() if '__pyx_id' in name and __PYX_ID__ != name]
    exists = get_cookie(__PYX_ID__) is not None
    pyx_id = None
    if not exists:
        pyx_id = get_random_name()
        set_cookie(__PYX_ID__, pyx_id)
        set_dom(pyx_id)

    result = str(__html__(children=body))
    if exists and not _ids_to_remove:
        return result

    response = make_response(result)
    for _id in _ids_to_remove:
        set_cookie(_id, '', response, expires=0)
    if not exists:
        set_cookie(__PYX_ID__, pyx_id, response)
    return response


handle_requests(__APP__, '/pyx', lambda r, kw: render_error(traceback=r, **kw), lambda _id: get_from_dom(_id)())


def run_app(*a, **k):
    return __APP__.run(*a, **(k or dict(debug=True)))

# TODO: add FastAPI app
