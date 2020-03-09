from opentracing.mocktracer import MockTracer
import tornado_opentracing
from tornado_opentracing import ScopeManager

tracing = tornado_opentracing.TornadoTracing(MockTracer(ScopeManager()))

print('scope manager used is:: ', ScopeManager)