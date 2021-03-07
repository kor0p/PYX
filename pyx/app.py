import os
from pyx import DEFAULT_TAG, render, run_app
from pyx.utils.app import __index__


tags_set = []
__pyx__ = lambda: ''
__PYX_FILE__ = os.environ.get('__PYX__') or '.'
try:
    exec(f'from {__PYX_FILE__} import *')
    exec(f'from {__PYX_FILE__} import __pyx__')
except ImportError as e:
    print(e)

__pyx__ = DEFAULT_TAG.update(name='pyx')(__pyx__)


@__index__
def index():
    return render(__pyx__())


run_app()
