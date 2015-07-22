"""
A deprecation warning can be issued when
a decorated function is called.
"""
import functools
import warnings


def deprecated(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        warnings.warn("Deprecated: {}".format(fn.__name__),
                      category=DeprecationWarning)
        return fn(*args, **kwargs)
    return inner


@deprecated
def hello():
    print("hello!")


if __name__ == '__main__':
    # Use `python -Wd filename` to see the warning.
    hello()
