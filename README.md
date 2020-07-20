# xctf

## Prerequisite

* pycryptodome
* ropper(?)
* pwntools(?)

## install

```bash
pip install setup.py
export TEMPLATE_DIR="/path/to/dir" # or set -x TEMPLATE_DIR /path/to/dir
mkdir $TEMPLATE_DIR/ # if you haven't made dir
cp templates/exploit_template $TEMPLATE_DIR/
```

## usage

```bash
make_exploit.py -e executable -l libc.so.6  # create new exploit.py
```