from flask import Flask, request, jsonify, abort, make_response
from flask.json import loads

__cookies__ = {}
__requests__ = {}


def create_app(name='<pyx>'):
    return Flask(name)


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
    return response


def create_request(salt_id, key, value):
    if salt_id not in __requests__:
        __requests__[salt_id] = {}
    __requests__[salt_id][key] = value


def get_request(salt_id, key):
    return __requests__.get(salt_id, {}).get(key)


def _from_request(target, html):
    return jsonify(dict(
        target=target,
        html=str(html)
    ))


def handle_requests(app, request_prefix, on_error, rerender):
    @app.route(request_prefix + '/<name>', methods=['GET', 'POST'])
    def __pyx__requests__(name):
        _error_status = 500
        req = get_request(get_cookie(app.__PYX_ID__), name)
        kw = dict(request.args) | dict(loads(request.data))
        try:
            if not req:
                _error_status = 400
                raise ConnectionError('Bad Request')
            _id = kw.pop('id')
            print(req(**kw))
            return _from_request(_id, rerender(_id))
        except Exception as error:
            return abort(make_response(_from_request('error', on_error(str(error), kw)), 500))
