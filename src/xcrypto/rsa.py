from Crypto.Util.number import isPrime
from xcrypto.mod import inv
from xcrypto.rcf import to_rcf, rcf_to_frac

def euler_phi(p, q):
    if not isPrime(p) or not isPrime(q):
        ValueError("2 number must be prime")

    return (p - 1) * (q - 1)


def dec(c, d, n):
    return pow(c, d, n)


def dec_pq(c, p, q, e):
    n = p * q
    phi = euler_phi(p, q)
    d = inv(e, phi)
    return dec(c, d, n)


def wiener_rcf(rcf_tuple, index):
    rcf_list = list(rcf_tuple)[0:index + 1]
    if index % 2 == 0:
        rcf_list[-1] += 1

    return rcf_list


def wiener(c, n, e):
    ret = []
    rcf = to_rcf((e, n))

    for index in range(len(rcf)):
        frac = rcf_to_frac(wiener_rcf(rcf, index))
        k = frac[0]  # numerator
        d = frac[1]  # denominator

        # check k and d
        if e * d % k == 1:
            ret.append(dec(c, d, n))

    return ret