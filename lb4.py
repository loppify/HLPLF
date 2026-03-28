class NumericString:
    def __init__(self, value):
        val_str = str(value)
        if not val_str.isdigit():
            raise ValueError("Only digits allowed")
        self.value = val_str

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, NumericString):
            return int(self.value) == int(other.value)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return NumericString(int(self.value) + int(other.value))

    def __sub__(self, other):
        res = int(self.value) - int(other.value)
        if res < 0:
            raise ValueError("Negative result not allowed")
        return NumericString(res)

    def __mul__(self, other):
        return NumericString(int(self.value) * int(other.value))

    def __floordiv__(self, other):
        divisor = int(other.value)
        if divisor == 0:
            raise ZeroDivisionError("Division by zero")
        return NumericString(int(self.value) // divisor)

    def __invert__(self):
        return NumericString(self.value[::-1])


def run_tests():
    s1 = NumericString("123")
    s2 = NumericString("45")
    s3 = NumericString("123")

    print(f"Eq 1: {s1 == s3}")
    print(f"Eq 2: {s1 == s2}")

    print(f"Ne 1: {s1 != s2}")
    print(f"Ne 2: {s1 != s3}")

    print(f"Add 1: {s1 + s2}")
    print(f"Add 2: {NumericString('10') + NumericString('20')}")

    print(f"Sub 1: {s1 - s2}")
    print(f"Sub 2: {NumericString('50') - NumericString('50')}")

    print(f"Mul 1: {s1 * NumericString('2')}")
    print(f"Mul 2: {NumericString('10') * NumericString('10')}")

    print(f"Div 1: {s1 // s2}")
    print(f"Div 2: {NumericString('1000') // NumericString('10')}")

    print(f"Inv 1: {~s1}")
    print(f"Inv 2: {~NumericString('1002')}")


if __name__ == "__main__":
    run_tests()
