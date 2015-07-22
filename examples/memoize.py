import functools


def memoize(fn):
    cache = {}

    @functools.wraps(fn)
    def inner(n):
        if n not in cache:
            cache[n] = fn(n)
        return cache[n]
    return inner
