class SciNotNumber:
    def __init__(self, exponent: int, mantissa: int) -> None:
        self.exponent = exponent
        self.mantissa = mantissa

    def __pow__(self, other):
        exp = self.exponent 