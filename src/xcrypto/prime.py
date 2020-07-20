from xcrypto.num_util import *
from Crypto.Util.number import isPrime


def is_prime(n):
    """
    wrapper of Crypto.Util.number.isPrime
    `isPrime()` returns `1` when number is odd prime
    I hate this!!
    """
    res = isPrime(n)

    if res == 1 or res == True:
        return True

    return False


def fermat_method(n):
    a = int_sqrt(n)

    if a**2 == n:
        return (a, a)

    a += 1
    b_pow_2 = a ** 2 - n

    while not is_square(b_pow_2):
        a += 1
        b_pow_2 = a ** 2 - n

    b = int_sqrt(b_pow_2)

    return (a + b, a - b)
