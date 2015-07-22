import collections
import datetime
import functools

from pprint import pprint


def printargs(fn):
    """
    Decorator that can be applied to any function and will
    print out the values of the parameters passed into it.
    """
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if args:
            pprint(args)
        if kwargs:
            pprint(kwargs)
    return inner


def prevent_none(fn):
    """
    Decorator that causes an assertion error
    if the function returns None.
    """
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        retval = fn(*args, **kwargs)
        if retval is None:
            raise AssertionError
        else:
            return retval
    return inner


def cache_n(maxsize):
    """
    Decorator that caches the n most recent return values, so that
    the function does not have to be invoked again.
    """
    def decorator(fn):
        cache = {}
        hist = collections.deque(maxlen=maxsize)

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            if maxsize < 1:
                return fn(*args, **kwargs)

            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = fn(*args, **kwargs)

            if key in hist:
                hist.remove(key)

            if len(hist) == maxsize:
                del cache[hist.pop()]

            hist.appendleft(key)
            return cache[key]
        return inner
    return decorator


def cache_seconds(n):
    """
    Decorator that caches all return values of the function
    for n seconds.
    """
    def decorator(fn):
        cache = {}

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()

            if key in cache and (cache[key][0] + n) > now:
                res = cache[key][1]
            else:
                res = fn(*args, **kwargs)

            cache[key] = (now, res)
            return res

        return inner
    return decorator


class store_seconds:
    """
    Decorator that stores all return values the function
    generated for n seconds.
    """
    __retvals = []

    def __init__(self, n):
        self._time = datetime.datetime.now()
        self._delta = datetime.timedelta(seconds=n)
        # Clean return values.
        if store_seconds.__retvals:
            store_seconds.__retvals = []

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            retval = fn(*args, **kwargs)
            now = datetime.datetime.now()
            if now < (self._time + self._delta):
                store_seconds.__retvals.append(retval)
            return retval
        return decorated

    @staticmethod
    def get_retvals():
        return store_seconds.__retvals


def retry_function(times, delay):
    """
    Decorator that makes retries the function n times with delay m
    between retries if the function throws an exception. If after
    n retries the function has still not succeeded, re-raise the
    exception.
    """
    def decorator(fn):

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            for _ in range(times):
                try:
                    retval = fn(*args, **kwargs)
                    success = True
                except Exception, err:
                    error = err
                    success = False

                if success:
                    return retval
                else:
                    time.sleep(delay)
            raise error

        return inner
    return decorator


if __name__ == '__main__':
    import sys
    import time
    import unittest

    class TestPrintargs(unittest.TestCase):

        def setUp(self):
            @printargs
            def fn(*args, **kwargs):
                pass

            self.test_fn = fn

        def init_stdout_check(self):
            if not hasattr(sys.stdout, 'getvalue'):
                self.fail("Need to run in a buffered mode.")
            return sys.stdout.getvalue().strip()

        def test_args_printed(self):
            self.test_fn(14, 15)
            output = self.init_stdout_check()
            self.assertEqual(output, '(14, 15)')

        def test_kwargs_printed(self):
            self.test_fn(foo='bar', spam='eggs')
            output = self.init_stdout_check()
            self.assertEqual(output, "{'foo': 'bar', 'spam': 'eggs'}")

        def test_args_and_kwargs_printed(self):
            self.test_fn(42, what='answer')
            output = self.init_stdout_check()
            self.assertEqual(output, "(42,)\n{'what': 'answer'}")

    class TestPreventNone(unittest.TestCase):

        def setUp(self):
            @prevent_none
            def fn(val):
                if type(val) == str:
                    return True

            self.test_fn = fn

        def test_fn_returns_true_if_str(self):
            self.assertTrue(self.test_fn('hello!'))

        def test_fn_raises_assertion_err(self):
            self.assertRaises(AssertionError, self.test_fn, 1)

    # !!! TODO: figure out how to properly test `cache_n`.
    # class TestMemoizeNvals(unittest.TestCase):

    #     def setUp(self):

    #         # Something O(2^n) to better see the difference.
    #         def fn(num):
    #             if num <= 1:
    #                 return num
    #             return fn(num - 1) + fn(num - 2)

    #         self.test_fn = fn

    #         # Simulate `cache_n` with different cache size.
    #         self.test_fn0 = cache_n(0)(fn)        # no caching
    #         self.test_fn10 = cache_n(10)(fn)      # size=10

    #     def timeit(self, fn, val):
    #         start_time = time.time()
    #         fn(val)
    #         return time.time() - start_time

    #     def test_with_caching_works_faster(self):
    #         num = 30
    #         time1 = self.timeit(self.test_fn, num)
    #         time2 = self.timeit(self.test_fn10, num)
    #         # self.assertTrue(time1 > time2)
    #         self.assertEqual(time1, time2)

    #     def test_cache_size_equals_zero(self):
    #         num = 30
    #         time1 = self.timeit(self.test_fn, num)
    #         time2 = self.timeit(self.test_fn0, num)
    #         # self.assertTrue(time1 == time2)
    #         # self.assertEqual(float("%.2f" % time1), float("%.2f" % time2))
    #         self.assertEqual(time1, time2)

    # Run tests.
    unittest.main(module=__name__, buffer=True, exit=False)
