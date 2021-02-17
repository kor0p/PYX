import os
import json
from pyx import cached_tag, render_error, Tag, div
from pyx import (  # importing extra data for pyx render
    __requests__,
    __html__,
    __DOM__,
)
from flask import Flask, request, jsonify, abort, make_response
__APP__ = Flask(__name__)
tags_set = []


__PYX_FILE__ = os.environ.get("__PYX__")
exec(f'from {__PYX_FILE__} import *')
try:
    exec(f'from {__PYX_FILE__} import __pyx__')
except ImportError:
    def __pyx__():
        pass


def _from_request(target, html):
    return jsonify(dict(
        target=target,
        html=str(html)
    ))


@__APP__.route('/pyx/<name>', methods=['GET', 'POST'])
def __pyx__requests__(name):
    req = __requests__.get(name)
    kw = dict(request.args) | dict(json.loads(request.data))
    if req:
        _id = kw.pop('id')
        print(req(**kw))
        tag_name = req.__qualname__.split('.')[0].lower()
        if local_tag := locals().get(tag_name):
            _id = str(hash(local_tag))
        return _from_request(_id, __DOM__[_id]())
    else:
        return abort(make_response(_from_request('error', render_error(**kw)), 500))


rules = dict((r.rule, r.endpoint) for r in __APP__.url_map.iter_rules())

if '/' not in rules:
    @__APP__.route('/')
    def index():
        return str(__html__(children=__pyx__()))
else:
    print(f'index route exists, using {rules["/"]} endpoint')

__APP__.run(debug=True)
