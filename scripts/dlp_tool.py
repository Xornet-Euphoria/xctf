from argparse import ArgumentParser
from xcrypto.prime import is_prime, factorize_by_factordb
from xlog import XLog


def create_parser():
    description = "Specify prime or order."
    parser = ArgumentParser(description=description)
    parser.add_argument("-p", "--prime", help="modulus prime number", type=int)
    parser.add_argument("-o", "--order", help="order of group", type=int)
    parser.add_argument("-f", "--factor_limit", help="the limit of large factor", type=int, default=10**14)
    parser.add_argument("-a", "--answer_limit", help="the limit of answer", type=int)
    return parser


if __name__ == "__main__":
    logger = XLog("DLP")
    parser = create_parser()
    args = parser.parse_args()

    prime = args.prime
    order = args.order
    factor_limit = args.factor_limit
    answer_limit = args.answer_limit

    if prime is None and order is None:
        parser.print_help()
        exit(0)

    if prime is not None:
        if not is_prime(prime):
            logger.error("You specified a composite number as a prime number")
            exit(1)
        if order is None:
            order = prime - 1

    factors = factorize_by_factordb(order)

    is_ph_effective = True
    effective_order = 1
    for i, f_e in enumerate(factors):
        factor, exponent = f_e
        label = ""
        if factor_limit is not None and pow(factor, exponent) > factor_limit:
            label = " <- large factor"
            is_ph_effective = False
        else:
            effective_order *= pow(factor, exponent)
        print(f"[+] factor #{i}: {factor}^{exponent} {label}")

    if is_ph_effective:
        logger.info("Pohlig-Hellman Algorithm seems effective!!")
    else:
        if answer_limit is not None and answer_limit < effective_order:
            logger.info(f"Pohlig-Hellman Algorithm seems effective, because the answer seems less than {effective_order}.")
        else:
            logger.info("Pohlig-Hellman Algorithm seems ineffective...")

