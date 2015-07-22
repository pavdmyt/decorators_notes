"""
A common use of decorators is to time the execution of functions.
`timeit` decorator in below example, when applied to functions,
prints out the execution time of every invocation.
"""
import functools
import random
import time


# !!! TODO: think about how it could be reimplemented as a class
#           decorator.
def timeit(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        start_time = time.time()
        retval = fn(*args, **kwargs)
        duration = time.time() - start_time
        print("{}: {} sec".format(fn.__name__, duration))
        return retval
    return inner


@timeit
def bubble_sort(seq):
    seq = seq[:]
    for i in range(len(seq)):
        for j in range(len(seq) - 1 - i):
            if seq[j] > seq[j+1]:
                seq[j], seq[j+1] = seq[j+1], seq[j]
    return seq


if __name__ == '__main__':
    test_seq1 = [random.randrange(500) for _ in range(10**3)]
    test_seq2 = [random.randrange(500) for _ in range(10**4)]

    bubble_sort(test_seq1)
    bubble_sort(test_seq2)
