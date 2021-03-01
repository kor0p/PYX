from .children import *
from .core import *
from .dom import *
from .JSON import *
from .rand import *
from .state import *

"""

def get_cookies():
    data = request.cookies
    updatedData, data_type = Page.getData(pathname, data)

    response = make_response()
    for cookie in bad_cookies:
        response.set_cookie(cookie, '', expires=0)
    if data_type == 'cookie':
        data.update(**(updatedData or {}))
        expire_date = datetime.datetime.strptime('2100', '%Y')
        for name, cookie in data.items():
            response.set_cookie(name, dumps(cookie), expires=expire_date)
        return response
    elif data_type == 'body':
        return dumps(updatedData, data_type)
"""


__extra__ = JSON()
