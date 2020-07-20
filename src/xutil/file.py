from pathlib import Path


def get_top_bytes(filepath, n=16):
    f = open(filepath, "rb")
    ret = f.read(n)
    f.close()

    return ret


def get_all_file(dirpath="./"):
    p = Path(dirpath)
    return [child for child in p.iterdir() if child.is_file()]