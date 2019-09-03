class Equasion:
    def __init__(self, power, coeffs):
        self.power = power
        self.coeffs = coeffs
        if len(coeffs) - 1 != power:
            raise Exception

    def __call__(self, x):
        return sum(self.coeffs[self.power - i] * x**i for i in range(self.power + 1))

    def solve(self, error=0.00000001):
        current_x = 0
        current_y = self.__call__(curent_x)

        while abs(current_y) - error > 0:

            x += random.uniform(0, 1)


a = Equasion(2, (123, 32, 1))


