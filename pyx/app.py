import os
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


l = locals()
for tag_name in tags_set:
    if _tag := l.get(tag_name):
        if tag_name[:2] == tag_name[-2:] == '__':
            l[tag_name] = cached_tag.update(name=tag_name[2:-2])(_tag)
        else:
            l[tag_name] = cached_tag(_tag)
    else:
        l[tag_name] = Tag(name=tag_name)(div)


def _from_request(target, html):
    return jsonify(dict(
        target=target,
        html=str(html)
    ))


@__APP__.route('/pyx/<name>')
def __pyx__requests__(name):
    req = __requests__.get(name)
    kw = dict(request.args)
    if req:
        _id = kw.pop('id')
        print(req(**kw))
        tag_name = req.__qualname__.split('.')[0].lower()
        if local_tag := l.get(tag_name):
            #pass
            _id = str(hash(local_tag))
            #return _from_request(__DOM__[], local_tag())
        return _from_request(_id, __DOM__[_id]())
    else:
        return abort(make_response(_from_request('error', render_error(**kw)), 500))
        # return abort(500, description=_from_request('error', render_error(**kw)))


rules = dict((r.rule, r.endpoint) for r in __APP__.url_map.iter_rules())

if '/' not in rules:
    @__APP__.route('/')
    def index():
        return str(__html__(children=__pyx__()))
else:
    print(f'index route exists, using {rules["/"]} endpoint')

__APP__.run(debug=True)
