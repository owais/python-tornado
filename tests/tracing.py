import asyncio
import pytest
from opentracing.mocktracer import MockTracer
from tornado import version_info as tornado_version
import tornado.gen
import tornado.web
import tornado.testing
import tornado_opentracing
from tornado_opentracing import ScopeManager, trace_context

tracing = tornado_opentracing.TornadoTracing(MockTracer(ScopeManager()))