import asyncio
import inspect
from functools import partial

import wrapt
import functools

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
        tracing = self

        class Descriptor(object):
            def __init__(self, f):
                self.wrapped = f

            async def __call__(self, handler, *args, **kwargs):

                if tracing._trace_all:
                    return self.wrapped(handler, *args, **kwargs)

                with trace_context():
                    try:
                        tracing._apply_tracing(handler, list(attributes))
                        print('\n\n')

                        # Run the actual function.
                        #if inspect.iscoroutinefunction(self.wrapped):
                        #    result = await self.wrapped(handler, *args, **kwargs)
                        #else:
                        #    result = self.wrapped(handler, *args, **kwargs)
                        result = self.wrapped(handler, *args, **kwargs)
                        if result is not None and inspect.isawaitable(result):
                            print('result:: ', result)
                            result = await result

                        # if it has `add_done_callback` it's a Future,
                        # else, a normal method/function.
                        if callable(getattr(result, 'add_done_callback', None)):
                            callback = functools.partial(
                                    tracing._finish_tracing_callback,
                                    handler=handler)
                            result.add_done_callback(callback)
                        else:
                            tracing._finish_tracing(handler)

                    except Exception as exc:
                        tracing._finish_tracing(handler, error=exc)
                        raise


            def __get__(self, instance, owner):
                return partial(self.__call__, instance)

        return Descriptor

        def decorator(original):
            instance = original.__self__

            def wrapper(instance, *args, **kwargs):
                return original(*args, **kwargs)
                # return original.__func__(original.__self__, *args, **kwargs)

            bound_wrapper = instance.__get__(instance, instance.__class__)
            setattr(instance, method_name, bound_wrapper)
            return wrapper

        return decorator


        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            if self._trace_all:
                return wrapped(*args, **kwargs)

            handler = instance

            with trace_context():
                try:
                    self._apply_tracing(handler, list(attributes))
                    print('\n\n')

                    # Run the actual function.
                    #if inspect.iscoroutinefunction(wrapped):
                    #    result = await wrapped(*args, **kwargs)
                    #else:
                    #    result = wrapped(*args, **kwargs)
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


    def trace_async_await(self, *attributes):
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
                    print('\n\n')

                    # Run the actual function.
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
