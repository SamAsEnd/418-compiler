from nodes.Value import Value


class Number(Value):
    def __init__(self, number: int):
        if abs(number) > 2 ** 31:
            raise SyntaxError(str(number) + ' number is out of range')
        self.number = number

    def __str__(self):
        return str(self.number)
