# xctf

## Prerequisite

* python 3.8 or higher
* pycryptodome
* factordb-python

## install

```
$ python setup.py install
$ export TEMPLATE_DIR="/path/to/dir" # or set -x TEMPLATE_DIR /path/to/dir
$ mkdir $TEMPLATE_DIR/ # if you haven't made dir
$ cp templates/exploit_template $TEMPLATE_DIR/
```

## usage

```
$ make_exploit.py --help
usage: make_exploit.py [-h] [-e ELF] [-l LIBC] [--host HOST] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -e ELF, --elf ELF     ELF path
  -l LIBC, --libc LIBC  libc path
  --host HOST           target address
  -p PORT, --port PORT  target port
```

## License

MIT