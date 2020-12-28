from xcrypto.finitefield import FiniteField, Element
from xcrypto.mod import crt
from math import ceil, sqrt
from Crypto.Random.random import randint


class ECPoint:
    def __init__(self, x, y, curve):
        self.x = Element(x, curve.p) if x is not None else None
        self.y = Element(y, curve.p) if x is not None else None
        if not curve.on_curve((x, y)):
            raise ValueError(f"({x}, {y}) is not on curve: {curve}")
        self.curve = curve

    def unpack(self):
        if self.is_o():
            return (None, None)
        else:
            return (self.x.x, self.y.x)

    def __eq__(self, point):
        return self.curve == point.curve and self.x == point.x and self.y == point.y

    def __str__(self):
        _x = self.x if self.x is not None else "inf"
        _y = self.y if self.y is not None else "inf"
        return f"({_x}, {_y})"

    def raise_different_curve_err(self, point):
        if self.curve != point.curve:
            raise ValueError(
                "Calculation is failed because they are over different curve")

    def is_o(self):
        return self.x is None and self.y is None

    def __neg__(self):
        if self.is_o():
            return self
        return self.__class__(self.x.x, -self.y.x, self.curve)

    def __add__(self, point):
        self.raise_different_curve_err(point)
        if self.is_o():
            return point

        if point.is_o():
            return self

        if self.x == point.x and self.y == -point.y:
            return self.curve.get_o()

        if self == point:
            s = (Element(3, self.curve.p) * self.x**2 + self.curve.a) / \
                (Element(2, self.curve.p) * self.y)
        else:
            s = (point.y - self.y) / (point.x - self.x)

        ret_x = s**2 - self.x - point.x
        ret_y = s * (self.x - ret_x) - self.y
        return self.__class__(ret_x.x, ret_y.x, self.curve)

    def __rmul__(self, scalar):
        if isinstance(scalar, Element):
            scalar = int(scalar)
        elif not isinstance(scalar, int):
            raise ValueError("scalar must be `int` or `Element` of `FiniteField`")
        ret = self.curve.get_o()
        twice_point = self
        while scalar > 0:
            if (scalar & 1) == 1:
                ret += twice_point
            twice_point += twice_point
            scalar >>= 1

        return ret


# y^2 = x^3 + ax + b: over f_p
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = Element(a, p)
        self.b = Element(b, p)
        self.p = p
        self.order = None  # todo: calculating order

    def __str__(self):
        return f"y^2 = x^3 + {self.a}x + {self.b} over F_{self.p}"

    def __eq__(self, curve):
        return self.p == curve.p and self.a == curve.a and self.b == curve.b

    def __ne__(self, curve):
        return not (self == curve)

    def set_order(self, order):
        self.order = order

    def is_order_set(self):
        return self.order is not None

    def on_curve(self, point):
        _x, _y = point
        if _x is None and _y is None:
            return True
        if _x is None or _y is None:
            return False

        x, y = Element(_x, self.p), Element(_y, self.p)
        return y**2 == x**3 + self.a * x + self.b

    def get_o(self):
        return ECPoint(None, None, self)


class ECDSA:
    def __init__(self, ec: EllipticCurve, g: ECPoint, q: ECPoint, d: int=None) -> None:
        if not ec.is_order_set():
            raise ValueError("order is not set")
        self.curve = ec
        self.g = g
        self.q = q

        self.is_secret_set = False
        if d is not None:
            self.set_secret(d)
            self.is_secret_set = True
        else:
            self.d = None

    def set_secret(self, d: int) -> None:
        self.d = Element(d, self.curve.order)
        if d*self.g != self.q:
            raise ValueError("invalid secret")

    # z must be int
    def sign(self, z: int) -> tuple:
        if not self.is_secret_set:
            raise Exception("secret is not set")
        n = self.curve.order
        k = Element(randint(2, n-1), n)
        r = Element((int(k)*self.g).unpack()[0], n)
        s = (Element(z, n) + r*self.d) / k

        return (int(r), int(s))

    def verify(self, r: int, s: int, z: int) -> bool:
        n = self.curve.order
        r, s, z = Element(r, n), Element(s, n), Element(z, n)
        u, v = z / s, r / s
        kg = int(u)*self.g + int(v)*self.q
        return kg.unpack()[0] == int(r)


def bsgs(G, target, order, log=False):
    m = ceil(sqrt(order))

    d = {}
    jG = G.curve.get_o()
    for j in range(m):
        _x, _y = jG.unpack()
        d[_x] = (_y, j)
        jG += G

    if log:
        print("[+] table is created.")

    minus_mG = -(m * G)
    rhs = target
    for i in range(m):
        _x, _y = rhs.unpack()
        if _x in d and _y == d[_x][0]:
            return i * m + d[_x][1]

        rhs += minus_mG

    return None


def ec_pohlig_hellman(g, y, factorized_orders, log=False):
    order = 1
    for i, t in enumerate(factorized_orders):
        if isinstance(t, int):
            t = (t, 1)
            factorized_orders[i] = t

        order *= pow(t[0], t[1])
    xs = []
    problem = []

    for q, e in factorized_orders:
        if log:
            print(f"[+]: attempting {q}^{e}")
        q_e = pow(q, e)
        exp_i = order // q_e
        g_i = exp_i * g
        y_i = exp_i * y
        x_i = bsgs(g_i, y_i, q_e, log)
        if x_i is None:
            if log:
                print("[+] exponent is not found...")
                return None
        xs.append(x_i)
        problem.append([x_i, q_e])

    return crt(problem)
