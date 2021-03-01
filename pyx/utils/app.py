import os
from typing import Optional, Callable, TypeVar

Response = TypeVar('Response')
APP = TypeVar('APP')

__APP__ = os.environ.get('__APP__', 'flask')

create_app:      Callable[[str], APP]
get_cookies:     Callable[[], Optional[dict[str, str]]]
get_cookie:      Callable[[str, Optional[str]], str]
set_cookie:      Callable[[str, str, Optional[Response]], Response]
create_request:  Callable[[str, Callable], None]
get_request:     Callable[[str], Optional[Callable]]
handle_requests: Callable[[APP, str, Callable[[str, dict], str], Callable[[str], str]], Response]

make_response: Callable[[str], Response]

if __APP__ == 'flask':
    from pyx.apps.app_flask import *
else:
    raise ImportError('Cannot find renderer app')
