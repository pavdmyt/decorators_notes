def decorator1(fn):
    print("decorator1")

    def inner1(*args, **kwargs):
        print("inner1")
        return fn(*args, **kwargs)
    return inner1


def decorator2(fn):
    print("decorator2")

    def inner2(*args, **kwargs):
        print("inner2")
        return fn(*args, **kwargs)
    return inner2


# This is the syntactic sugar for equivalent:
# foo = decorator1(decorator2(foo))
@decorator1
@decorator2
def foo():
    print("foo")


if __name__ == '__main__':
    foo()

    # $ python decorators_chain.py
    #
    # decorator2
    # decorator1
    # inner1
    # inner2
    # foo
