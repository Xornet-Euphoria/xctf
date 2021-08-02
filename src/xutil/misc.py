def conn_info(s: str):
    raw_l = s.split(" ")
    if len(raw_l) < 2:
        raise ValueError("Invalid command: please specify host and port")

    if len(raw_l) == 3:
        if raw_l[0] != "nc":
            raise ValueError("Invalid command: please start `nc`")
        raw_l = raw_l[1:]

    host = raw_l[0]
    try:
        port = int(raw_l[1])
    except:
        raise ValueError("port must be a number")

    return (host, port)