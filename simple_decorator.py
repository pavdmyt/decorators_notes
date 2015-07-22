import functools


def foo(fn):
    @functools.wraps(fn)
    def inner():
        print("About to call function.")
        fn()
        print("Finished calling function.")
    return inner


# This is the syntactic sugar for equivalent:
# bar = foo(bar)
@foo
def bar():
    """
    `bar` function.
    """
    print("Calling function bar.")


if __name__ == '__main__':
    bar()

    # $ python simple_decorator.py
    #
    # About to call function.
    # Calling function bar.
    # Finished calling function.
