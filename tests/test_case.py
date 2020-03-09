import sys


if sys.version_info >= (3, 3):
    from ._test_case_py33 import AsyncHTTPTestCase  # noqa
else:
    from ._test_case_base import BaseAsyncHTTPTestCase as AsyncHTTPTestCase  # noqa
