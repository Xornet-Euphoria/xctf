from hashlib import sha1
from xlog import XLog
from .elf import search_elf


libc_database = [
    {
        "SHA1": "ed475285eed517355f0e6976502d15df2237fc6f",
        "version": "2.31",
        "gadgets": [945379, 945382, 945385],
        "main_arena.top": 0x1ebbe0
    },
    {
        "SHA1": "18292bd12d37bfaf58e8dded9db7f1f5da1192cb",
        "version": "2.27",
        "gadgets": [324293, 324386, 1090444],
        "main_arena.top": 0x3ebca0
    }
]


def _sha1(data):
    return sha1(data).hexdigest()


def _sha1file(file):
    with open(file, "rb") as f:
        data = f.read()
    return _sha1(data)


def search_libc(dirname="./"):
    ret = []
    elfs = search_elf()

    # identified from hash
    for elf in elfs:
        sha1hash = _sha1file(elf)

        if get_libc_by_hash(sha1hash) is not None:
            ret.append(elf)

    # identified from name
    if len(ret) == 0:
        for elf in elfs:
            if "libc" in str(elf):
                ret.append(elf)

    return ret


def analyze_libc(libc_path):
    sha1hash = _sha1file(libc_path)

    libc = get_libc_by_hash(sha1hash)

    if libc is None:
        XLog("LIBC").warning(f"Database doesn't have the data of this libc (sha1: {sha1hash})")

    return libc


def get_libc_by_hash(hash):
    for libc in libc_database:
        if libc["SHA1"] == hash:
            return libc

    return None


def get_libc_by_ver(version):
    for libc in libc_database:
        if libc["version"] == version:
            return libc

    return None
