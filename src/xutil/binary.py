def get_bytes(filepath, start, end=None):
    if end is not None and start > end:
        raise ValueError("`start` must be smaller than `end`")

    ret = b""
    with open(filepath, "rb") as f:
        ret = f.read()

    data_length = len(ret)
    if end is None:
        end = data_length

    if start >= data_length or end > data_length:
        return None

    return ret[start:end]


def extract_bytes(filepath, outpath, start, end=None):
    extracted_bytes = get_bytes(filepath, start, end)

    with open(outpath, "wb") as f:
        f.write(extracted_bytes)

    return