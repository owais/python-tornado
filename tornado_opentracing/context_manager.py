from tornado import version_info as tornado_version

if tornado_version < (6, 0):
    from opentracing.scope_managers.tornado import (
        tracer_stack_context as trace_context
    )
else:

    def trace_context():
        return _NoopContextManager()


class _NoopContextManager(object):
    def __enter__(self):
        pass

    def __exit__(self, *_):
        pass
