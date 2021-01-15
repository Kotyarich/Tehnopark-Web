from django.conf import settings
from django.test.runner import DiscoverRunner

try:
    import cProfile as profile
except ImportError:
    import profile


class ProfilingRunner(DiscoverRunner):

    def run_tests(self, *args, **kwargs):
        s = super(ProfilingRunner, self)

        profile.runctx(
            'run_tests(*args, **kwargs)',
            {
                'run_tests': s.run_tests,
                'args': args,
                'kwargs': kwargs
            },
            {},
            getattr(settings, 'TEST_PROFILE', None))
