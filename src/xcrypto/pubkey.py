from xcrypto import rsa
from xcrypto.mod import is_quadratic_residue, legendre_symbol


def rsa_dec(c: int, d: int, n: int) -> int:
    return rsa.dec(c, d, n)


def rsa_dec_pq(c: int, p: int, q: int, e: int) -> int:
    return rsa.dec_pq(c, p, q, e)


def goldwasser_micali_dec(cs, p):
    ret = 0
    for c in cs:
        ret <<= 1
        if not is_quadratic_residue(c, p):
            ret += 1

    return ret
