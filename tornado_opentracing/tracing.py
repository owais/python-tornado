import sys

from tornado import version_info as tornado_version


if sys.version_info >= (3, 5) and tornado_version >= (5, 0):
    from .tracing_async import TornadoTracing
else:
    from .tracing_base import BaseTornadoTracing as TornadoTracing
 