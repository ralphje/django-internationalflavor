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
