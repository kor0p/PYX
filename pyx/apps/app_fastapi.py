import uvicorn

from os import path
from pathlib import Path
from typing import Optional

from json import loads
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse

make_response = HTMLResponse

__cookies__ = {}
__requests__ = {}

_app: Optional[FastAPI] = None


class HashableRequest(Request):
    def __hash__(self):
        return hash(tuple(self.scope.items()))


request: Request = HashableRequest({'type': 'http', 'headers': ''})


class SessionError(ConnectionError):
    pass


class RequestError(ConnectionError):
    pass


def _run(*, name, **kwargs):
    kwargs.setdefault('host', '0.0.0.0')
    kwargs.setdefault('reload', True)
    kwargs.setdefault('debug', False)
    kwargs.setdefault('workers', 3)
    return uvicorn.run(name + ':app', **kwargs)


def create_app(name='<pyx>', **kwargs):
    global _app
    _app = FastAPI(name=name, **kwargs)
    _app.run = _run
    _app.mount(
        '/pyx/static',
        StaticFiles(
            directory=path.relpath(
                (Path(path.abspath(__file__)) / '../../static').resolve()
            )
        ),
        name='static',
    )
    return _app


def get_cookies():
    return request.cookies | __cookies__.get(request, {})


def get_cookie(key, default=None):
    return request.cookies.get(key, default) or __cookies__.get(request, {}).get(key)


def set_cookie(key, value, response: Response = None, **kwargs):
    if response is None:
        if request not in __cookies__:
            __cookies__[request] = {}
        __cookies__[request][key] = value
        return
    response.set_cookie(key=key, value=value, **kwargs)
    if request in __cookies__:
        del __cookies__[request]
    return response


def create_request(salt_id, key, value):
    if salt_id not in __requests__:
        __requests__[salt_id] = {}
    __requests__[salt_id][key] = value


def get_request(salt_id, key):
    return __requests__.get(salt_id, {}).get(key)


def _from_request(target, html):
    return dict(target=target, html=str(html))


def handle_requests(request_prefix, on_error, rerender):
    @_app.get(request_prefix + '/{name}')
    @_app.post(request_prefix + '/{name}')
    async def __pyx__requests__(__request__: Request, name: str):
        global request
        request = __request__
        _error_status = 500
        kw = dict(__request__.query_params) | dict(loads(await __request__.body()))
        try:
            try:
                req = get_request(_app._get_session_id(), name)
            except SessionError:
                raise SessionError(_app.__PYX_ID__)
            if not req:
                _error_status = 400
                raise RequestError('Bad Request')
            _id = kw.pop('id')
            print(req(**kw))
            return _from_request(_id, rerender(_id))
        except Exception as error:
            return JSONResponse(
                _from_request('error', on_error(str(error), kw)), _error_status
            )

    return __pyx__requests__


def __index__(func):
    rules = dict((r.path, r.endpoint) for r in _app.routes)

    if '/' not in rules:
        _app.get('/')(_app.post('/')(func))
    else:
        print(f'index route exists, using {rules["/"]} endpoint')


__all__ = [
    'SessionError',
    'RequestError',
    'create_app',
    'get_cookies',
    'get_cookie',
    'set_cookie',
    'create_request',
    'get_request',
    'handle_requests',
    '__index__',
    'make_response',
]
