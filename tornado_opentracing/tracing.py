import sys

if sys.version_info >= (3, 5):
    from .tracing_async import TornadoTracing
else:
    from .tracing_base import TornadoTracing