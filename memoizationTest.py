from functools import wraps
from time import perf_counter
import sys


def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper


@memoize
def fibo(n) -> int:
    if n < 2:
        return n
    return fibo(n - 1) + fibo(n - 2)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    start = perf_counter()

    f = fibo(30)
    end = perf_counter()

    print(f)
    print(f"Time: {end - start} seconds")
