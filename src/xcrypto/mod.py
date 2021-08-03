from math import gcd
from functools import reduce
from Crypto.Util.number import isPrime
from xcrypto.num_util import prod, list_gcd, lcm


# I hate `%` operator...
def mod_f(x, n):
    return x % n


def inv(x, n):
    return pow(x, -1, n)


def neg(x, n):
    return -x % n


def is_equivalent(a, b, n):
    return (a - b) % n == 0


def ext_euclid(a, b):
    x_0, x_1, y_0, y_1 = 1, 0, 0, 1
    sign = 1
    while b != 0:
        r = a % b
        q = a // b
        a = b
        b = r
        tmp_x = x_1
        tmp_y = y_1
        x_1 = q * x_1 + x_0
        y_1 = q * y_1 + y_0
        x_0 = tmp_x
        y_0 = tmp_y
        sign = -sign

    g = a
    # a * (sign*x_0) + b * (-sign*y_0) = g
    return (sign * x_0, -sign * y_0, g)


# chinese reminder theorem
def _is_two_crt_solvable(a_1, m_1, a_2, m_2):
    g = gcd(m_1, m_2)
    return is_equivalent(a_1, a_2, g)


def two_crt(a_1, m_1, a_2, m_2):
    # todo: 互いに素で無い場合でも解けることの確認とその解法
    if not _is_two_crt_solvable(a_1, m_1, a_2, m_2):
        return None
    u, v, g = ext_euclid(m_1, m_2)
    l = lcm(m_1, m_2)

    k = (a_2 - a_1) // g
    assert a_1 + k * m_1 * u == a_2 - k * m_2 * v

    return mod_f(a_1 + k * m_1 * u, l)


def _two_crt_tuple(t1, t2):
    return (two_crt(t1[0], t1[1], t2[0], t2[1]), lcm(t1[1], t2[1]))


def crt(problem):
    a_list = [x[0] for x in problem]
    m_list = [x[1] for x in problem]

    for i in range(len(m_list)):
        for j in range(len(m_list)):
            if i == j:
                continue
            if not _is_two_crt_solvable(a_list[i], m_list[i], a_list[j], m_list[j]):
                return None

    return reduce(lambda x, y: _two_crt_tuple(x, y), problem)[0]


# old code (this code did not use `reduce` and is non-functional)
"""
def crt(problem):
    eq_count = len(problem)
    a_list = [x[0] for x in problem]
    m_list = [x[1] for x in problem]

    for i in m_list:
        for j in m_list:
            if i == j:
                continue
            if gcd(i, j) != 1:
                raise ValueError("any 2 modulo pair must be coprime each other")

    m_all_prod = prod(m_list)
    m_star_list = [m_all_prod // m for m in m_list]

    t_list = [ext_euclid(m_list[i], m_star_list[i])[1]
              for i in range(eq_count)]

    answer = 0
    for i in range(eq_count):
        answer += (a_list[i] * m_star_list[i] * t_list[i])

    return answer % m_all_prod
"""


def is_quadratic_residue(a, p):
    if a % p == 0:
        return True

    return legendre_symbol(a, p) == 1


def legendre_symbol(a, p):
    if not isPrime(p) or p == 2:
        raise ValueError("p must be a odd prime number")

    if a % p == 0:
        return 0

    ret = pow(a, (p-1) // 2, p)

    return ret if ret == 1 else -1


def get_q_s(p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    return (q, s)


def get_nonresidue(p):
    ret = 2
    while is_quadratic_residue(ret, p):
        ret += 1

    return ret


def mod_sqrt(a, p):
    if not is_quadratic_residue(a, p):
        return ()

    if a == 0:
        return (a, )

    if (p - 3) % 4 == 0:
        k = (p - 3) // 4
        no_sign_sol = pow(a, -k, p)
        return (no_sign_sol, -no_sign_sol % p)

    return tonelli_shanks(a, p)


def tonelli_shanks(a, p):
    if not is_quadratic_residue(a, p):
        return ()

    if a == 0:
        return (0, )

    q, s = get_q_s(p)
    z = get_nonresidue(p)
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q+1) // 2, p)

    while True:
        if t == 1:
            return (r, neg(r, p))

        i = m
        for j in range(1, m):
            if pow(t, pow(2, j), p) == 1:
                i = j
                break

        b = pow(c, pow(2, m - i - 1), p)
        b_pow = pow(b, 2, p)
        m, c, t, r = i, b_pow, t * b_pow % p, r * b % p
