class countcalls(object):
    """
    Decorator that keeps track of the number of times
    the function is called.
    """
    __instances = {}

    def __init__(self, f):
        self.__f = f
        self.__num_calls = 0
        countcalls.__instances[f] = self

    def __call__(self, *args, **kwargs):
        self.__num_calls += 1
        return self.__f(*args, **kwargs)

    def count(self):
        return self.__num_calls

    @staticmethod
    def counts():
        return dict([(f.__name__, countcalls.__instances[f].__num_calls)
                    for f in countcalls.__instances])


@countcalls
def foo():
    pass


if __name__ == '__main__':
    for i in range(10):
        foo()

    print(foo.count())          # prints "10"
    print(countcalls.counts())  # prints "{'foo': 10}"
