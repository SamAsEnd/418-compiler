import random

from lib.nodes import *

tmp = Variable('1temp1')
variables = [tmp.name]

strings = {}


def offset(var: Variable) -> int:
    return (variables.index(var.name) + 1) * 4


def val(value: Value) -> str:
    return 'DWORD PTR [rbp-%d]' % offset(value) \
        if isinstance(value, Variable) else str(value.number)


def jmp(condition: Condition) -> str:
    if isinstance(condition, EqualTo):
        return 'jne'
    elif isinstance(condition, GreaterThan):
        return 'jle'
    elif isinstance(condition, GreaterOrEqualTo):
        return 'jl'
    elif isinstance(condition, LessThan):
        return 'jge'
    elif isinstance(condition, LessOrEqualTo):
        return 'jg'
    else:
        return 'je'


def generate_asm(stmt: Statement):
    if isinstance(stmt, VarDeclare):
        variables.append(stmt.variable.name)
        return generate_asm(Assignment(stmt.variable, stmt.expression))
    elif isinstance(stmt, Assignment):
        if isinstance(stmt.expression, Value):
            return 'mov eax, %s\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % \
                   (val(stmt.expression), offset(stmt.variable))
        elif isinstance(stmt.expression, Addition):
            return 'mov eax, %s\n' \
                   'add eax, %s\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % (
                       val(stmt.expression.first_operand),
                       val(stmt.expression.second_operand),
                       offset(stmt.variable))
        elif isinstance(stmt.expression, Subtraction):
            return 'mov eax, %s\n' \
                   'sub eax, %s\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % (
                       val(stmt.expression.first_operand),
                       val(stmt.expression.second_operand),
                       offset(stmt.variable))
        elif isinstance(stmt.expression, Multiplication):
            return 'mov eax, %s\n' \
                   'imul eax, %s\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % (
                       val(stmt.expression.first_operand),
                       val(stmt.expression.second_operand),
                       offset(stmt.variable))
        elif isinstance(stmt.expression, Division):
            return 'mov eax, %s\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' \
                   'mov eax, %s\n' \
                   'cdq\n' \
                   'idiv DWORD PTR [rbp-%d]\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % (
                       val(stmt.expression.second_operand),
                       offset(tmp),
                       val(stmt.expression.first_operand),
                       offset(tmp),
                       offset(stmt.variable))
        elif isinstance(stmt.expression, Modulus):
            return 'mov eax, %s\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' \
                   'mov eax, %s\n' \
                   'cdq\n' \
                   'idiv DWORD PTR [rbp-%d]\n' \
                   'mov DWORD PTR [rbp-%d], edx\n' % (
                       val(stmt.expression.second_operand),
                       offset(tmp),
                       val(stmt.expression.first_operand),
                       offset(tmp),
                       offset(stmt.variable))
    elif isinstance(stmt, Comment):
        return '# ' + stmt.string
    elif isinstance(stmt, CompoundStatement):
        code = ''
        for stmt in stmt:
            code += generate_asm(stmt)
        return code
    elif isinstance(stmt, Conditional):
        end_label = 'label_jmp_end_' + str(random.randint(0, 9999999))
        else_label = 'label_jmp_else_' + str(random.randint(0, 9999999))

        code = 'mov eax, %s\n' \
               'cmp eax, %s\n' \
               '%s %s\n' % (
                   val(stmt.condition.first_operand), val(stmt.condition.second_operand),
                   jmp(stmt.condition), else_label)

        code += generate_asm(stmt.true)
        code += ('jmp ' + end_label + '\n')

        code += else_label + ':\n'
        code += generate_asm(stmt.false)
        code += ('jmp ' + end_label + '\n')

        return code + end_label + ':\n'
    elif isinstance(stmt, Loop):
        end_label = 'label_loop_end_' + str(random.randint(0, 9999999))
        loop_label = 'label_loop_' + str(random.randint(0, 9999999))

        code = loop_label + ':\n'
        code += 'mov eax, %s\n' \
                'cmp eax, %s\n' \
                '%s %s\n' % (
                    val(stmt.condition.first_operand), val(stmt.condition.second_operand),
                    jmp(stmt.condition), end_label)

        code += generate_asm(stmt.true)
        code += ('jmp ' + loop_label + '\n')

        return code + end_label + ':\n'
    elif isinstance(stmt, WriteString):
        str_label = 'string_' + str(random.randint(0, 9999999))

        strings[str_label] = stmt.string.string + '\n'

        return 'mov rax, 1\n' \
               'mov rdi, 1\n' \
               'mov rsi, offset %s\n' \
               'mov rdx, %d\n' \
               'syscall\n' % (str_label, len(stmt.string.string.strip().strip('"')) + 1)

    elif isinstance(stmt, WriteValue):
        return 'mov rdi, offset integer\n' \
               'mov eax, %s\n' \
               'mov rsi, 0\n' \
               'mov esi, eax\n' \
               'mov rax, 0\n' \
               'call printf\n' % val(stmt.variable)

        # return 'mov edi, buffer\n' \
        #        'mov esi, %s\n' \
        #        'mov edx, 0\n' \
        #        'mov eax, 0\n' \
        #        'call int2str\n' \
        #        '' \
        #        'mov rdx, rax\n' \
        #        'mov rax, 1\n' \
        #        'mov rdi, 1\n' \
        #        'mov rsi, offset buffer\n' \
        #        'syscall\n' % val(stmt.variable)

    elif isinstance(stmt, Read):
        return 'mov eax, 0\n' \
               'mov rdi, offset integer\n' \
               'mov rsi, offset number\n' \
               'call scanf\n' \
               'mov eax, number\n' \
               'mov %s, eax\n' % (val(stmt.variable))
    else:
        raise Exception(stmt.__class__)


def generator(ast):
    code = open('src/lib/lib.asm').read()

    for stmt in ast:
        code += generate_asm(stmt) + '\n'

    code += 'mov rax, 60\nmov rdi, 0\nsyscall\n\n'

    # code += 'section .data\n'
    # code += 'section .data\n'

    for label in strings.keys():
        code += '%s: .string "%s\\n"\n' % (label, strings[label].strip().strip('"'))

    code += 'integer: .string "%d"\n'
    # code += 'buffer: .string "' + '\0' * 15 + '"\n'

    return code
