# only supporting x86_64
from capstone import Cs, CS_ARCH_X86, CS_MODE_64


def get_disassembler(b: bytes, offset: int=0):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    return md.disasm(b, offset=offset)


if __name__ == "__main__":
    # xor rax, rax; inc rax
    b = b'H1\xc0H\xff\xc0'
    md = get_disassembler(b, 0x114514)

    for insn in md:
        print(f"0x{insn.address:x}: {insn.mnemonic}, {insn.op_str}")