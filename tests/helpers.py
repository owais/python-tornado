import sys

import pytest
from tornado import version_info as tornado_version


def skip_generator_contextvars_on_tornado6(func):
    return pytest.mark.skipif(
        tornado_version >= (6, 0, 0),
        reason=(
            'tornado6 has a bug (#2716) that '
            'prevents contextvars from working.'
        )
    )(func)


def skip_generator_contextvars_on_py34(func):
    return pytest.mark.skipif(
        sys.version_info.major == 3 and sys.version_info.minor == 4,
        reason=('does not work on 3.4 with tornado context stack currently.')
    )(func)


def skip_no_async_await(func):
    return pytest.mark.skipif(
        sys.version_info < (3, 5) or tornado_version < (5, 0),
        reason=(
            'async/await is not supported on python older than 3.5 '
            'and tornado older than 5.0.'
        )
    )(func)
