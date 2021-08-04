from xcrypto.num_util import *
from math import isqrt, sqrt, floor
from Crypto.Util.number import isPrime, getPrime
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



def next_prime(n):
    if not isinstance(n, int):
        raise ValueError("`n` must be a intager")

    if n < 2:
        return 2
    if n == 2:
        return 3

    n += (n % 2 + 1)

    while True:
        if isPrime(n):
            return n
        n += 2


def get_unsafe_prime(pbit, qbit=24, exponents=False):
    while True:
        q_set = set()
        q_set.add(2)
        p = 2
        while True:
            q = getPrime(qbit)
            if q in q_set:
                continue
            q_set.add(q)
            p *= q
            _pbit = p.bit_length()
            if _pbit > pbit:
                p //= q
                break

        _pbit = p.bit_length()
        if _pbit < pbit:
            _bit = pbit - _pbit
            while True:
                q = getPrime(_bit)
                if q not in q_set:
                    q_set.add(q)
                    p *= q
                    break
            while p.bit_length() < pbit:
                p *= 2

        p += 1
        if isPrime(p):
            if exponents:
                phi = p - 1
                exponents = []
                two_count = 0
                while phi % 2 == 0:
                    two_count += 1
                    phi //= 2

                exponents.append((2,two_count))
                for q in q_set:
                    if q == 2:
                        continue
                    exponents.append((q,1))
                return p, exponents
            return p


def fermat_method(N, attempt=None):
    a = isqrt(N) + 1
    while attempt != 0:
        b2 = a * a - N
        if isqrt(b2)**2 == b2:
            return (a - isqrt(b2), a + isqrt(b2))
        a += 1
        if attempt is not None:
            attempt -= 1
    return None


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
