from nodes import *


class Parser:
    @classmethod
    def parse_comment(cls, tokens):
        return Comment(tokens[0])

    @classmethod
    def parse_expression(cls, tokens):
        if len(tokens) == 1:
            try:
                return Number(int(tokens[0]))
            except ValueError:
                return Variable(tokens[0])
        elif tokens[1] == '+':
            return Addition(cls.parse_expression(tokens[0:1]), cls.parse_expression(tokens[2:3]))
        elif tokens[1] == '-':
            return Subtraction(cls.parse_expression(tokens[0:1]), cls.parse_expression(tokens[2:3]))
        elif tokens[1] == '*':
            return Multiplication(cls.parse_expression(tokens[0:1]), cls.parse_expression(tokens[2:3]))
        elif tokens[1] == '/':
            return Division(cls.parse_expression(tokens[0:1]), cls.parse_expression(tokens[2:3]))
        elif tokens[1] == '%':
            return Modulus(cls.parse_expression(tokens[0:1]), cls.parse_expression(tokens[2:3]))

    @classmethod
    def parse_var_declare(cls, tokens):
        if len(tokens) == 1:
            exp = Number(0)
        else:
            exp = cls.parse_expression(tokens[1:])

        return VarDeclare(Variable(tokens[0]), exp)

    @classmethod
    def parse_assignment(cls, tokens):
        exp = cls.parse_expression(tokens[1:])

        return Assignment(Variable(tokens[0]), exp)

    @classmethod
    def parse_condition(cls, tokens):
        first_op = cls.parse_expression([tokens[0]])
        second_op = cls.parse_expression([tokens[2]])

        if tokens[1] == '>':
            return GreaterThan(first_op, second_op)
        elif tokens[1] == '>=':
            return GreaterOrEqualTo(first_op, second_op)
        elif tokens[1] == '<':
            return LessThan(first_op, second_op)
        elif tokens[1] == '<=':
            return LessOrEqualTo(first_op, second_op)
        elif tokens[1] == '~':
            return EqualTo(first_op, second_op)
        else:
            return NotEqualTo(first_op, second_op)

    @classmethod
    def parse_the_rest(cls, tokens_group, split_at):
        split_at.append('end')

        nest = 0
        counter = 0

        while counter < len(tokens_group):
            tokens = tokens_group[counter]

            if nest == 0 and tokens[0] in split_at:
                true = cls.parse(tokens_group[:counter])
                if tokens[0] == 'end':
                    return true, CompoundStatement()
                elif tokens[0] == 'elif':
                    return true, cls.parse_options(tokens_group[counter:])
                else:
                    return true, cls.parse(tokens_group[counter + 1:len(tokens_group) - 1])

            if tokens[0] in ['if', 'while']:
                nest += 1
            elif tokens[0] == 'end' and nest > 0:
                nest -= 1

            counter += 1

    @classmethod
    def parse_options(cls, tokens_group):
        condition = cls.parse_condition(tokens_group[0][1])
        true, rest = cls.parse_the_rest(tokens_group[1:], ['elif', 'else'])

        return Conditional(condition, true, rest)

    @classmethod
    def parse_while(cls, tokens_group):
        condition = cls.parse_condition(tokens_group[0][1])
        true, rest = cls.parse_the_rest(tokens_group[1:], [])

        return Loop(condition, true)

    @classmethod
    def parse_write(cls, tokens):
        if tokens[0].startswith('"'):
            return WriteString(String(tokens[0]))
        else:
            return WriteValue(cls.parse_expression(tokens))

    @classmethod
    def parse_writeln(cls, tokens):
        group = CompoundStatement()

        if tokens[0].startswith('"'):
            group.add(WriteString(String(tokens[0])))
        else:
            group.add(WriteValue(cls.parse_expression(tokens)))

        group.add(WriteString(String('"\\n"')))

        return group

    @classmethod
    def parse_read(cls, tokens):
        return Read(Variable(tokens[0]))

    @classmethod
    def parse(cls, tokens):
        SIMPLE_PARSERS = {
            'comment': cls.parse_comment,
            'var declare': cls.parse_var_declare,
            'assignment': cls.parse_assignment,
            'write': cls.parse_write,
            'writeln': cls.parse_writeln,
            'read': cls.parse_read,
        }

        statements = CompoundStatement()

        buffer = []
        nested = 0
        counter = 0

        while counter < len(tokens):
            name, token = tokens[counter]
            if len(buffer) == 0 and name in SIMPLE_PARSERS.keys():
                statements.add(SIMPLE_PARSERS[name](token))
            else:
                buffer.append(tokens[counter])

                if name in ['if', 'while']:
                    nested += 1
                elif name == 'end':
                    if nested == 1:
                        if buffer[0][0] == 'if':
                            statements.add(cls.parse_options(buffer))
                        elif buffer[0][0] == 'while':
                            statements.add(cls.parse_while(buffer))
                        buffer.clear()
                        nested = 0
                    else:
                        nested -= 1

            counter += 1

        if len(buffer) != 0:
            raise RuntimeError('Error: You forgot to and "end" somewhere')

        return statements
