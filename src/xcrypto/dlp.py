from functools import reduce
from math import ceil, sqrt
from Crypto.Util.number import isPrime
from xcrypto.mod import crt, prod


def baby_step_giant_step(g, y, p, q=None):
    if not q:
        q = p

    if y <= 0 or y >= p:
        raise ValueError("y must be greater than 0 and less than p")
    if q > p:
        raise ValueError("q must be less or equal than p")

    m = ceil(sqrt(q))
    baby_step_j_dic = {}
    for j in range(m):
        baby_step_j_dic[pow(g, j, p)] = j

    gamma = y
    g_pow_minus_m = pow(g, -m, p)

    for i in range(m):
        if i != 0:
            gamma *= g_pow_minus_m
            gamma %= p
        if gamma in baby_step_j_dic:
            return i * m + baby_step_j_dic[gamma]


# required: list of prime factors 
# the factor of list is tuple: (base, exponent)
# ex. p = 73 (phi(p) = 72 = 2**3 * 3**2), factorized_phi_list = [(2, 3), (3, 2)]
def pohlig_hellman(g, y, p, factorized_phi_list, log=False):
    if isPrime(p):
        phi_p = p - 1
    else:
        phi_p = 1
        for t in factorized_phi_list:
            phi_p *= pow(t[0], t[1])
    xs = []
    problem = []

    for q, e in factorized_phi_list:
        if log:
            print("[+]: trying", q)
        q_e = pow(q, e)
        exp_i = phi_p // q_e
        g_i = pow(g, exp_i, p)
        y_i = pow(y, exp_i, p)
        x_i = baby_step_giant_step(g_i, y_i, p, q_e)
        if x_i is not None:
            xs.append(x_i)
            problem.append([x_i, q_e])

    return crt(problem)


def get_order(g: int, p: int, phi_exponents) -> int:
    phi = 1
    for q, e in phi_exponents:
        phi *= (q**e)

    order = phi

    while True:
        is_divisor = False
        for q, e in phi_exponents:
            _order = order // q
            if pow(g, _order, p) == 1:
                order = _order
                is_divisor = True

        if not is_divisor:
            break

    return order