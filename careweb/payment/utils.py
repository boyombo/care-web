from random import sample

REF = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"


def get_reference():
    return "".join(sample(REF, 30))
