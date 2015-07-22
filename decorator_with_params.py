import functools


def print_num(n):
    """
    Decorator with parameters, prints the number passed
    into it before calling the function.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            print(n)
            return fn(*args, **kwargs)
        return inner
    return decorator


# This is the syntactic sugar for equivalent:
# hello = print_num(5)(hello)
@print_num(5)
def hello():
    print("Hello!")


if __name__ == '__main__':
    hello()

    # $ python decorator_with_params.py
    #
    # 5
    # Hello!
