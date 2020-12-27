from xcrypto.num_util import *
from math import sqrt, floor
from Crypto.Util.number import isPrime
from factordb.factordb import FactorDB


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


def factorize_by_factordb(n):
    sc = FactorDB(n)
    sc.connect()
    raw_factorized = sc.get_factor_from_api()
    ret = []
    for factor in raw_factorized:
        s_base, exponent = factor
        ret.append((int(s_base), exponent))

    return ret


"""
below codes are not for CTF
"""


def create_sieve(n):
    sieve = [True for _ in range(n + 1)]
    sieve[0] = False
    sieve[1] = False
    for i in range(2, floor(sqrt(n)) + 1):
        if not sieve[i]:
            continue

        for j in range(i**2, n+1, i):
            sieve[j] = False

    return sieve


def create_spf_sieve(n):
    sieve = [i for i in range(n + 1)]
    for i in range(2, floor(sqrt(n)) + 1):
        if sieve[i] != i:
            continue

        for j in range(i**2, n+1, i):
            if sieve[j] == j:
                sieve[j] = i

    return sieve


def __factorize_submodule(n, sieve):
    ret = {}
    if n == 0:
        ret[0] = 0
        return
    if n == 1:
        ret[1] = 1
        return
    while n != 1:
        spf = sieve[n]
        n //= spf
        if not spf in ret:
            ret[spf] = 0

        ret[spf] += 1

    return ret


def factorize(n):
    sieve = create_spf_sieve(n)
    return __factorize_submodule(n, sieve)


def all_factorize(n):
    sieve = create_spf_sieve(n)
    ret = [{} for _ in range(n + 1)]
    for i in range(n+1):
        ret[i] = __factorize_submodule(i, sieve)

    return ret
