import sys
from tornado import version_info as tornado_version

use_generators = False

if sys.version_info < (3, 7):
    use_generators = True


#if tornado_version < (6, 0, 0, 0):
#    from opentracing.scope_managers.tornado import TornadoScopeManager as ScopeManager
#else:
#    if sys.version_info >= (3, 7):
#        from opentracing.scope_managers.contextvars import ContextVarsScopeManager as ScopeManager
#    elif sys.version_info >= (3, 0):
#        from opentracing.scope_managers.asyncio import AsyncioScopeManager as ScopeManager