from itertools import combinations, zip_longest, repeat
from functools import reduce
from operator import mul
from string import printable


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks
    Taken from itertools documentation (really powerful stuff):
    https://docs.python.org/3.6/library/itertools.html#itertools-recipes

    >>> grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


num = 1087943696176439095600323762148055792209594928798662843208446383247024

try:
    from sympy import factorint
    factorisation = factorint(num)
except ImportError:
    factorisation = {
        2: 4,
        409: 1,
        3917: 1,
        11802520621: 1,
        3596125089166804548750482737481944979533469020291403: 1
    }

factors = []
for divisor, power in factorisation.items():
    factors.extend(repeat(divisor, power))
"""
factors == [
    2, 2, 2, 2, 409, 3917, 11802520621,
    3596125089166804548750482737481944979533469020291403
]
"""

for factor_count in range(1, len(factors) + 1):
    """
    Going over every possible number of factors in message.
    (num == message*multiplier and we selecting only factors from the message)
    """

    for message_factorisation in set(combinations(factors, factor_count)):
        """
        Going over every possible combinations of factor_count factors.
        In fact there will be some repeated combinations due to 4
        '2's in factorization, that's why I use set to uniq-ify combinations.
        (That's an afterthought, to be honest)
        """

        message = reduce(mul, message_factorisation)
        """
        Calculating message - multiplying together every element in
        message_factorisation.

        operator.mul - '*' as a function. Equivalent to lambda a, b: a*b

        functools.reduce - operation from functional programming.
        It's simple, really:
        >>> reduce(mul, [1, 2, 3, 4])
        Is the same as
        >>> (((1*2)*3)*4)
        """

        message_hex = hex(message)[2:] # cutting "0x" from the number

        if len(message_hex) % 2 != 0:
            # only if contains whole number of bytes
            continue

        message_str = ''.join( # Join together all letters
            chr( # Now we have string 'A'
                int( # Now we have int 0x41
                    ''.join(byte), # Now we've got string '41'
                    16
                )
            )
            for byte in grouper(message_hex, 2)
            # byte is tuple of hex chars: ('4', '1')
        )

        if any(char not in printable for char in message_str):
            continue

        print(message_str)
