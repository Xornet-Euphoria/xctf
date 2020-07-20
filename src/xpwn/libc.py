from hashlib import sha1
from xlog import XLog


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


def analyze_libc(libc_path):
    f = open(libc_path, "rb")
    data = f.read()
    sha1hash = _sha1(data)

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
