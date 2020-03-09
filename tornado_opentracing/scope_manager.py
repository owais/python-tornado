import sys
from tornado import version_info as tornado_version

if tornado_version < (6, 0):
    from opentracing.scope_managers.tornado import TornadoScopeManager as ScopeManager  # noqa
else:
    if sys.version_info < (3, 7):
        from opentracing.scope_managers.asyncio import AsyncioScopeManager as ScopeManager  # noqa
    else:
        from opentracing.scope_managers.contextvars import ContextVarsScopeManager as ScopeManager  # noqa
