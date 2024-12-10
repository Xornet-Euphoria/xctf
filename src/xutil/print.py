import pprint
from typing import TypeAlias
from dataclasses import dataclass

default_bool: TypeAlias = bool | None


# context
@dataclass
class PrintCtx():
    print_original: bool = False
    return_original: bool = False

    def __post_init__(self):
        self.ctx_dict = {
            "print_original": self.print_original,
            "return_original": self.return_original
        }

    def __getitem__(self, key):
        return getattr(self, key)
    

    def __setitem__(self, key, value):
        return setattr(self, key, value)


_print_ctx = PrintCtx()


# utils for pring
def get_print_original(print_original: default_bool):
    return _print_ctx.print_original if print_original is None else print_original


# for used in external
def set_print_original(print_original: bool):
    _print_ctx.print_original = print_original


def get_return_original(return_original: default_bool):
    return _print_ctx.return_original if return_original is None else return_original


# for used in external
def set_return_original(return_original: bool):
    _print_ctx.return_original = return_original


def hook_print(x, f=None, *, print_original: default_bool=None, return_original: default_bool=None):
    print_original = get_print_original(print_original)
    return_original = get_print_original(return_original)

    ret = x if return_original else None
    if f is None:
        print(x)
    else:
        if print_original:
            print(f(x))
            print(x)
        else:
            print(f(x))

    return ret


def pp(x, *, return_original: default_bool=None):
    return_original = get_return_original(return_original)

    if return_original:
        pprint.pp(x)
        return x
    
    pprint.pp(x)


def dir_print(x, *, print_original: default_bool=None, return_original: default_bool=None):
    return hook_print(x, dir, print_original=print_original, return_original=return_original)


def len_print(x, *, print_original: default_bool=None, return_original: default_bool=None):
    return hook_print(x, len, print_original=print_original, return_original=return_original)


if __name__ == "__main__":
    l = [1,2,3]

    len_print(l)
    dir_print(l)

    set_print_original(True)
    set_return_original(True)

    res1 = len_print(l)
    res2 = dir_print(l)

    print(res1, res2)