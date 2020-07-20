from fractions import Fraction


def euclid(ab_tuple):
    a = ab_tuple[0]
    b = ab_tuple[1]
    return a // b, a % b


def to_rcf(ab_tuple):  # regular continued fraction
    rcf_list = []
    a = ab_tuple[0]
    b = ab_tuple[1]
    while True:
        euclid_result = euclid(tuple([a, b]))
        rcf_list.append(euclid_result[0])
        a = b
        b = euclid_result[1]

        if b == 1:
            rcf_list.append(a)
            break

    return tuple(rcf_list)


def rcf_to_frac(rcf_tuple):
    rcf_list = list(rcf_tuple)
    a = rcf_list.pop()
    while len(rcf_list) != 0:
        b = rcf_list.pop()
        a = b + Fraction(1, a)

    return (a.numerator, a.denominator)


if __name__ == '__main__':
    print(rcf_to_frac(to_rcf(tuple([42667, 64741]))))  # 42667/64741
