"""
The decorator below checks the types of the parameters passed into any
function and raises an AssertionError if they do not match.
"""
import functools


def accepts(*types):
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            for (t, a) in zip(types, args):
                assert isinstance(a, t)
            return fn(*args, **kwargs)
        return inner
    return decorator


@accepts(int)
def is_even(n):
    return n % 2 == 0


if __name__ == '__main__':
    print(is_even(10))
    print(is_even(5))
    print(is_even(3.5))
