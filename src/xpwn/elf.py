from xutil import get_all_file, get_top_bytes


def search_elf():
    ret = []
    files = get_all_file()
    for f in files:
        magic_bytes = get_top_bytes(f)
        if len(magic_bytes) < 4:
            continue
        if magic_bytes[0:4] == b"\x7fELF":
            ret.append(f)

    return ret
