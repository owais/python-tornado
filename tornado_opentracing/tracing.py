import sys

from tornado import version_info as tornado_version


use_async_tracing = sys.version_info >= (3, 5) and tornado_version >= (5, 0)

if use_async_tracing:
    from .tracing_async import TornadoTracing  # noqa
else:
    from .tracing_base import BaseTornadoTracing as TornadoTracing  # noqa
