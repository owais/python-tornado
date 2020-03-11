import sys

from tornado import version_info as tornado_version


use_async_tracing = sys.version_info >= (3, 5) and tornado_version >= (5, 0)

if use_async_tracing:
    from ._tracing_async_py35 import TornadoTracing  # noqa
else:
    from ._tracing import BaseTornadoTracing as TornadoTracing  # noqa
