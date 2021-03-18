from time import time as _time
from random import random as _random

from string import digits as _digits
from string import ascii_letters as _ascii_letters

def nonce():
    """
    Returns a new nonce to be used with the Piazza API.
    """
    nonce_part1 = _int2base(int(_time()*1000), 36) 
    nonce_part2 = _int2base(round(_random()*1679616), 36)
    return "{}{}".format(nonce_part1, nonce_part2)

# Code adapted from:
# https://stackoverflow.com/a/2267446/408734

_exradix_digits = _digits + _ascii_letters

def _int2base(x, base):
    """
    Converts an integer from base 10 to some arbitrary numerical base,
    and return a string representing the number in the new base (using
    letters to extend the numerical digits).

    :type     x: int
    :param    x: The integer to convert
    :type  base: int
    :param base: The base to convert the integer to
    :rtype: str
    :returns: String representing the number in the new base
    """
    
    if base > len(_exradix_digits):
        raise ValueError(
            "Base is too large: The defined digit set only allows for "
            "bases smaller than " + len(_exradix_digits) + "."
        )

    if x > 0:
        sign = 1
    elif x == 0:
        return _exradix_digits[0]
    else:
        sign = -1

    x *= sign
    digits = []

    while x:
        digits.append(
            _exradix_digits[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)
