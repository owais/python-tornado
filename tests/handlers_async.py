import sys

import tornado.web

if sys.version_info < (3, 5):
    from .handlers_coroutine import (
        AsyncScopeHandler, DecoratedAsyncHandler, DecoratedAsyncScopeHandler, DecoratedAsyncErrorHandler
    )



class noopHandler(tornado.web.RequestHandler):
    def get(self):
        pass


AsyncScopeHandler = noopHandler
DecoratedAsyncHandler = noopHandler
DecoratedAsyncScopeHandler = noopHandler
DecoratedAsyncErrorHandler = noopHandler