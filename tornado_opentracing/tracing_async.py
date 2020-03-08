import asyncio
import inspect
import wrapt

from .tracing_base import  BaseTornadoTracing
from .context_manager import trace_context


class TornadoTracing(BaseTornadoTracing):

    def trace(self, *attributes):
        """
        Function decorator that traces functions
        NOTE: Must be placed before the Tornado decorators
        @param attributes any number of request attributes
        (strings) to be set as tags on the created span
        """

        @wrapt.decorator
        async def wrapper(wrapped, instance, args, kwargs):
            if self._trace_all:
                return wrapped(*args, **kwargs)

            handler = instance

            with trace_context():
                try:
                    self._apply_tracing(handler, list(attributes))

                    # Run the actual function.
                    # result = wrapped(*args, **kwargs)

                    if inspect.iscoroutinefunction(wrapped):
                        result = await wrapped(*args, **kwargs)
                    else:
                        result = wrapped(*args, **kwargs)

                    # if it has `add_done_callback` it's a Future,
                    # else, a normal method/function.
                    if callable(getattr(result, 'add_done_callback', None)):
                        callback = functools.partial(
                                self._finish_tracing_callback,
                                handler=handler)
                        result.add_done_callback(callback)
                    else:
                        self._finish_tracing(handler)

                except Exception as exc:
                    self._finish_tracing(handler, error=exc)
                    raise

            return result

        return wrapper
