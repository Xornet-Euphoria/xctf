from xcrypto.num_util import list_gcd


def next_lcg(a, b, m, x):
    return (a * x + b) % m


# x_2 = (a * x_1 + b(unknown)) % b
def solve_only_b(a, x_1, x_2, m):
    return (x_2 - a * x_1) % m


def solve_a_and_b(x_1, x_2, x_3, m):
    y_2 = (x_3 - x_2) % m
    y_1 = (x_2 - x_1) % m

    a = (pow(y_1, -1, m) * y_2) % m
    b = solve_only_b(a, x_1, x_2, m)

    return (a, b)


# todo: stricter solver
def solve_a_b_m(x_list):
    if len(x_list) < 7:
        raise ValueError("7 random numbers are needed")

    y = []
    for i in range(6):
        y.append(x_list[i + 1] - x_list[i])

    z = []
    # i + j = 5
    z.append(y[1] * y[4] - y[2] * y[3])
    # i + j = 7
    z.append(y[2] * y[5] - y[3] * y[4])
    # i + j = 6
    z.append(y[2] * y[4] - y[1] * y[5])

    g = list_gcd(z)

    a, b = solve_a_and_b(x_list[1], x_list[2], x_list[3], g)

    return (a, b, g)
