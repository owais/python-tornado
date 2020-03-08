import sys
from tornado import version_info as tornado_version

use_generators = sys.version_info < (3, 7)

if use_generators:
    from .handlers_coroutine import (
        ScopeHandler, DecoratedAsyncHandler, DecoratedAsyncScopeHandler, DecoratedAsyncErrorHandler
    )
else:
    from .handlers_async import (
        ScopeHandler, DecoratedAsyncHandler, DecoratedAsyncScopeHandler, DecoratedAsyncErrorHandler
    )