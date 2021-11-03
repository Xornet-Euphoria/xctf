from Crypto.Util.number import isPrime
from xcrypto.mod import inv
from xcrypto.rcf import to_rcf, rcf_to_frac
from xcrypto.num_util import solve_quadratic_eq
from typing import Dict, List, Tuple, Union
from math import gcd


class RSACracker:
    def __init__(self, params: Dict, multiprime: bool=False) -> None:
        # support: int, digits ("114514")
        #   not support hex text ("0x114514")

        self.n = int(params["n"]) if "n" in params else None
        self.p = int(params["p"]) if "p" in params else None
        self.q = int(params["q"]) if "q" in params else None
        self.factors = []
        self.multiprime = multiprime
        if multiprime:
            if "factors" in params:
                for f in params["factors"]:
                    if isinstance(f, tuple) or isinstance(f, list):
                        self.factors((int(f[0]), int(f[1])))
                    else:
                        self.factors((int(f), 1))
        else:
            if self.p is not None:
                self.factors.append((self.p, 1))
            if self.q is not None:
                self.factors.append((self.q, 1))
        self.c = int(params["c"]) if "c" in params else None
        self.e = int(params["e"]) if "e" in params else None
        self.d = int(params["d"]) if "d" in params else None
        self.phi = int(params["phi"]) if "phi" in params else None
        self.p_plus_q = int(params["p+q"]) if "p+q" in params else None
        if self.p_plus_q is None and "p_plus_q" in params:
            self.p_plus_q = int(params["p_plus_q"])
        self.d_bound = None


    def add_factor(self, v: int, e: int=1) -> None:
        if self.n is not None and self.n % (v**e) != 0:
            raise ValueError("given value is not factor of n")
        self.factors.append((v, e))
        if len(self.factors) > 2:
            self.multiprime = True


    def add_factors(self, vs: List) -> None:
        for v in vs:
            if isinstance(v, int):
                self.add_factor(v)
            elif isinstance(v, tuple) or isinstance(v, list):
                if len(v) != 2:
                    raise ValueError("invalid factor format. Valid format: (<factor>, <exponent>).")
                self.add_factor(v[0], v[1])
            else:
                raise TypeError(f"the type of factor: {type(v)} is unsupported type")


    def check_and_decrypt(self, suggestion=False) -> Tuple[bool, Union[int, None]]:
        if self.c is None:
            return (False, None)

        if self.__check_parameters(["d", "n"]):
            return (True, self.__simple_decrypt())

        if self.__check_parameters(["e", "phi", "n"]):
            if self.__check_e_and_phi():
                return (True, self.__phi_decrypt())
            # todo: else pattern

        if self.multiprime:
            if self.__check_parameters(["factors", "e"]):
                if self.__check_factors():
                    return (True, self.__multiprime_decrypt())
        else:
            if self.__check_parameters(["p", "q", "e"]):
                if self.__check_factors():
                    return (True, self.__pq_decrypt())

            if self.__check_parameters(["p+q", "e", "n"]):
                return (True, self.__p_plus_q_decrypt())

            # todo: re-implement wiener's attack in this lib
            # if self.__check_parameters(["e", "n", "d_bound"]):
                # if self.__check_wiener():
                    # return (True, )

            # attack suggestion
            if suggestion:
                if self.__check_parameters(["e", "n", "d_bound"]):
                    if self.__check_boneh_durfee():
                        print("[+} Boneh-Durfee Attack seems to be effective, but it's not implemented sorry.")

        return (False, None)


    def __check_parameters(self, keys: List[str]) -> bool:
        table = {
            "n": self.n,
            "c": self.c,
            "e": self.e,
            "p": self.p,
            "q": self.q,
            "d": self.d,
            "phi": self.phi,
            "p+q": self.p_plus_q,
            "factors": self.factors,
            "d_bound": self.d_bound
        }

        for key in keys:
            if table[key] is None:
                return False

        return True


    def __check_factors(self) -> bool:
        if self.n is None:
            raise ValueError("self.n is not defined")

        _n = 1
        if self.multiprime:
            if self.factors is None:
                raise ValueError("self.factors is not defined")

            for f, e in self.factors:
                _n *= (f**e)

        else:
            if not self.__check_parameters(["p", "q"]):
                raise ValueError("self.factors is not defined")
            _n = self.p * self.q

        return self.n == _n


    def __check_e_and_phi(self) -> bool:
        return gcd(self.e, self.phi) == 1


    # attack suggestion
    def __check_wiener(self) -> bool:
        if self.d_bound < int(1/3 * pow(self.n, 1/4)):
            return True

        return False


    def __check_boneh_durfee(self) -> bool:
        if self.d_bound < int(pow(self.n, 0.292)):
            return True

        return False


    def __simple_decrypt(self) -> int:
        return dec(self.c, self.d, self.n)


    def __phi_decrypt(self) -> int:
        if gcd(self.e, self.phi) != 1:
            raise ValueError("e and phi must be coprime")
        self.d = pow(self.e, -1, self.phi)
        return self.__simple_decrypt()


    def __pq_decrypt(self) -> int:
        return dec_pq(self.c, self.p, self.q, self.e)


    def __p_plus_q_decrypt(self) -> int:
        p,q = p_plus_q_to_pq(self.n, self.p_plus_q)
        self.p = p
        self.q = q
        return self.__pq_decrypt()


    def __wiener_decrypt(self) -> int:
        raise NotImplementedError


    def __multiprime_decrypt(self) -> int:
        return dec_multiprime(self.c, self.factors, self.e)


def dec(c: int, d: int, n: int) -> int:
    return pow(c, d, n)


def dec_pq(c: int, p: int, q: int, e: int) -> int:
    if not isPrime(p) or not isPrime(q):
        raise ValueError("`p` and `q` must be a prime number")
    n = p * q
    phi = (p-1)*(q-1)
    d = inv(e, phi)
    return dec(c, d, n)


def dec_multiprime(c: int, factors: List[Tuple[int, int]], e: int) -> int:
    phi = 1
    n = 1
    for f, _e in factors:
        n *= (f**_e)
        phi *= (f**(_e-1) * (f-1))
    d = inv(e, phi)
    return dec(c, d, n)


def phi_to_pq(n: int, phi: int):
    if n <= phi:
        raise ValueError("phi must be (p-1)*(q-1)")

    p_plus_q = n - phi + 1

    return p_plus_q_to_pq(n, p_plus_q)


def p_plus_q_to_pq(n: int, p_plus_q: int) -> tuple:
    res = solve_quadratic_eq(1, -p_plus_q, n, True)

    if len(res) != 2:
        raise ValueError("no factor is found")

    p, q = res

    if p*q == n:
        return (p,q)

    raise ValueError("p * q != n, Please check n is product of two prime numbers and phi is correct")


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