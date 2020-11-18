from xcrypto.finitefield import FiniteField, Element


class ECPoint:
    def __init__(self, x, y, curve):
        self.x = Element(x, curve.p) if x is not None else None
        self.y = Element(y, curve.p) if x is not None else None
        if not curve.on_curve((x, y)):
            raise ValueError(f"({x}, {y}) is not on curve: {curve}")
        self.curve = curve

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

    def __str__(self):
        return f"y^2 = x^3 + {self.a}x + {self.b} over F_{self.p}"

    def __eq__(self, curve):
        return self.p == curve.p and self.a == curve.a and self.b == curve.b

    def __ne__(self, curve):
        return not (self == curve)

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
