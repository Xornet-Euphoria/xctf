class FiniteField:
    def __init__(self, p):
        self.p = p

    def __eq__(self, fp):
        return self.p == fp.p

    def __ne__(self, fp):
        return self.p != fp.p

    # for util (no need creating FiniteField instance)

    def inv(self, x):
        return pow(x, -1, self.p)


class Element:
    def __init__(self, x, p):
        self.x = x % p
        self.fp = FiniteField(p)

    def __int__(self):
        return self.x

    def __str__(self):
        return f"{self.x}"

    def int_to_elm(self, elm):
        if isinstance(elm, int):
            return self.to_same_fp_elm(elm)
        elif not isinstance(elm, Element):
            raise ValueError("`elm` must be int or Element")

        return elm

    def to_same_fp_elm(self, elm):
        return Element(elm, self.fp.p)

    def check_same_field(self, elm):
        return self.fp == elm.fp

    def raise_different_field_err(self, elm):
        if self.fp != elm.fp:
            raise ValueError(
                "Calculation is failed because they are over different field")

    def return_same_fp(self, x):
        return self.__class__(x, self.fp.p)

    def inv(self):
        return self.return_same_fp(pow(self.x, -1, self.fp.p))

    def __eq__(self, elm):
        if not self.check_same_field(elm):
            return False

        return self.x == elm.x

    def __neg__(self):
        return self.return_same_fp(-self.x)

    def __add__(self, elm):
        elm = self.int_to_elm(elm)
        self.raise_different_field_err(elm)
        return self.return_same_fp(self.x + elm.x)

    def __sub__(self, elm):
        elm = self.int_to_elm(elm)
        self.raise_different_field_err(elm)
        return self.return_same_fp(self.x - elm.x)

    def __mul__(self, elm):
        elm = self.int_to_elm(elm)
        self.raise_different_field_err(elm)
        return self.return_same_fp(self.x * elm.x)

    def __rmul__(self, elm):
        elm = self.int_to_elm(elm)
        self.raise_different_field_err(elm)
        return self.return_same_fp(self.x * elm.x)

    def __truediv__(self, elm):
        elm = self.int_to_elm(elm)
        self.raise_different_field_err(elm)
        return self.return_same_fp(self.x * elm.inv().x)

    def __pow__(self, exp):
        return self.return_same_fp(pow(self.x, exp, self.fp.p))
