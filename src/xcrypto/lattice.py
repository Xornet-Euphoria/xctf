from math import floor
from xcrypto.vector import dot_product


def gaussian_reduction(v1, v2):
    while True:
        if v2.norm() < v1.norm():
            v1, v2 = v2, v1

        m = floor(dot_product(v1, v2) / dot_product(v1, v1))
        if m == 0:
            return v1, v2

        v2 = v2 - m*v1
