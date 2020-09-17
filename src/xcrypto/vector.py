from math import sqrt


class Vector:
    def __init__(self, x):
        if not isinstance(x, list):
            raise TypeError("arg must be a list")
        self.nums = x
        self.length = len(x)

    def __str__(self):
        return str(self.nums)

    def __add__(self, y):
        if not isinstance(y, Vector):
            raise TypeError("arg must be a vector")

        if self.length != y.length:
            raise ValueError("the length of 2 vecs must be same.")

        z = [_x + y.nums[i] for i, _x in enumerate(self.nums)]

        return Vector(z)

    def __sub__(self, y):
        return self + (-1) * y

    def __mul__(self, a):
        if not isinstance(a, (int, float)):
            raise TypeError("arg must be number")

        z = [a * _x for _x in self.nums]

        return Vector(z)

    def __rmul__(self, a):
        if not isinstance(a, (int, float)):
            raise TypeError("arg must be number")

        z = [a * _x for _x in self.nums]

        return Vector(z)

    def norm(self):
        return sqrt(dot_product(self, self))

    def unpack(self):
        return self.nums


def dot_product(x, y):
    if x.length != y.length:
        raise ValueError("the length of 2 vecs must be same.")

    return sum([_x*_y for _x, _y in zip(x.nums, y.nums)])


def is_orthogonal(vs):
    for i, x in enumerate(vs):
        for j, y in enumerate(vs):
            if i == j:
                continue
            if dot_product(x, y) != 0:
                return False

    return True


def is_normalized(v):
    return v.norm() == 1.0


def is_orthonormal(vs):
    if not is_orthogonal(vs):
        return False

    for v in vs:
        if not is_normalized(v):
            return False

    return True


def normalize(v):
    return v * (1 / v.norm())


def calc_u(v, us):
    ret = v
    for u in us:
        c = dot_product(u, v) / dot_product(u, u)
        ret -= c * u

    return ret


def gram_schmidt(vs, do_normalize=False):
    us = []

    for v in vs:
        u = calc_u(v, us)
        if do_normalize:
            u = normalize(u)
        us.append(u)

    return us
