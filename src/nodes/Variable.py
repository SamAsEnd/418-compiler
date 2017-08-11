from nodes.Value import Value


class Variable(Value):
    KEYWORDS = 'var if elif else while do end read write writeln'.split()

    def __init__(self, name: str):
        if name in self.KEYWORDS:
            raise SyntaxError('Error: ' + name + ' is a keyword')
        self.name = name

    def __str__(self):
        return self.name
