class ValueCleaner(object):
    def __call__(self, value):
        """Returns the value that is cleaned for database usage"""
        return value

    def display_value(self, value):
        """Returns the value that can be used for display"""
        return self(value)


class UpperCaseValueCleaner(ValueCleaner):
    def __call__(self, value):
        """Returns the value that is cleaned for database usage"""
        if value is not None:
            return value.upper().replace(' ', '').replace('-', '').replace('.', '')
        return value


def _get_check_digit(to_check, factors, mod=11):
    """Method that calculates a check digit based on the following formula:

    (10x_1+9x_2+8x_3+7x_4+6x_5+5x_6+4x_7+3x_8+2x_9+x_10) mod [mod]
    where x_1 thru x_10 are values from to_check
    and 10..1 are values from factors

    Also known as the elfproef
    """
    return sum(int(to_check[i]) * factors[i] for i in range(len(factors))) % mod
