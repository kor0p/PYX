from flask import Flask, request, jsonify, abort, make_response
from flask.json import loads

__cookies__ = {}
__requests__ = {}

_app: Flask = None


class SessionError(ConnectionError):
    pass


class RequestError(ConnectionError):
    pass


def create_app(name='<pyx>', **kwargs):
    global _app
    _app = Flask(name, **kwargs)
    return _app


def get_cookies():
    return request.cookies | __cookies__.get(request, {})


def get_cookie(key, default=None):
    return request.cookies.get(key, default) or __cookies__.get(request, {}).get(key)


def set_cookie(key, value, response=None, **kwargs):
    if response is None:
        if request not in __cookies__:
            __cookies__[request] = {}
        __cookies__[request][key] = value
        return
    response.set_cookie(key, value, **kwargs)
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
    return jsonify(dict(target=target, html=str(html)))


def handle_requests(request_prefix, on_error, rerender):
    @_app.route(request_prefix + '/<name>', methods=['GET', 'POST'])
    def __pyx__requests__(name):
        _error_status = 500
        kw = dict(request.args) | dict(loads(request.data))
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
            return abort(
                make_response(
                    _from_request('error', on_error(str(error), kw)), _error_status
                )
            )

    return __pyx__requests__


def __index__(func):
    rules = dict((r.rule, r.endpoint) for r in _app.url_map.iter_rules())

    if '/' not in rules:
        _app.route('/')(func)
    else:
        print(f'index route exists, using {rules["/"]} endpoint')
