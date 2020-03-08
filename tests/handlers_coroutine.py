import tornado.web


class ScopeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def do_something(self):
        tracing = self.settings.get('opentracing_tracing')
        with tracing.tracer.start_active_span('Child'):
            tracing.tracer.active_span.set_tag('start', 0)
            yield tornado.gen.sleep(0.0)
            tracing.tracer.active_span.set_tag('end', 1)

    @tornado.gen.coroutine
    def get(self):
        tracing = self.settings.get('opentracing_tracing')
        span = tracing.get_span(self.request)
        assert span is not None
        assert tracing.tracer.active_span is span

        yield self.do_something()

        assert tracing.tracer.active_span is span
        self.write('{}')