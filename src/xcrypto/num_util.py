from math import ceil, gcd, isqrt, sqrt
from functools import reduce


def prod(num_list):
    return reduce(lambda x, y: x * y, num_list)


def list_gcd(num_list):
    return reduce(gcd, num_list)


def lcm(a, b):
    return a * b // gcd(a, b)


# return integer number less than or equal to pow(x, (1/n))
def int_nth_root(x, n):
    b_length = x.bit_length()
    ret_ceil = pow(2, ceil(b_length / n))
    ret_range = [1, ret_ceil]
    while True:
        ret_half = (ret_range[0] + ret_range[1]) // 2
        v = pow(ret_half, n)
        if v < x:
            if pow(ret_half + 1, n) > x:
                return ret_half
            ret_range[0] = ret_half
        elif v > x:
            ret_range[1] = ret_half
        elif v == x:
            return ret_half


def int_sqrt(x):
    return int_nth_root(x, 2)


def is_square(x):
    if x < 0:
        return False

    r = int_sqrt(x)

    return r**2 == x


# f = ax^2 + bx + c
def solve_quadratic_eq(a, b, c, int_sol=False):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return ()

    if int_sol:
        sqrt_d = isqrt(discriminant)
        if sqrt_d**2 != discriminant:
            return ()

        sol_l = []
        for sign in [-1,1]:
            numer = -b + sign * sqrt_d
            denom = 2*a

            if numer % denom == 0:
                sol_l.append(numer // denom)

        return sol_l

    sol_l = []
    for sign in [-1, 1]:
        numer = -b + sign * sqrt(discriminant)
        denom = 2*a

        sol_l.append(numer / denom)

    return sol_l
