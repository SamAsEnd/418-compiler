import random
from multiprocessing.managers import State

from lib.nodes import *

variables = []

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
            return 'mov eax, DWORD PTR [rbp-%d]\n' \
                   'imul eax, DWORD PTR [rbp-%d]\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % (
                       val(stmt.expression.first_operand),
                       val(stmt.expression.second_operand),
                       offset(stmt.variable))
        elif isinstance(stmt.expression, Division):
            return 'mov eax, DWORD PTR [rbp-%d]\n' \
                   'cdq\n' \
                   'idiv DWORD PTR [rbp-%d]\n' \
                   'mov DWORD PTR [rbp-%d], eax\n' % (
                       val(stmt.expression.first_operand),
                       val(stmt.expression.second_operand),
                       offset(stmt.variable))
        elif isinstance(stmt.expression, Modulus):
            return 'mov eax, DWORD PTR [rbp-%d]\n' \
                   'cdq\n' \
                   'idiv DWORD PTR [rbp-%d]\n' \
                   'mov DWORD PTR [rbp-%d], edx\n' % (
                       val(stmt.expression.first_operand),
                       val(stmt.expression.second_operand),
                       offset(stmt.variable))
    elif isinstance(stmt, Comment):
        return ''  # ''; ' + stmt.string
    elif isinstance(stmt, CompoundStatement):
        code = ''
        for stmt in stmt:
            code += generate_asm(stmt)
        return code
    elif isinstance(stmt, Conditional):
        end_label = 'JMP_END_' + random.randint(0, 9999999)
        else_label = 'JMP_ELSE_' + random.randint(0, 9999999)

        code = 'mov eax, DWORD PTR [rbp-4]\n' \
               'cmp eax, DWORD PTR [rbp-8]\n' \
               '%s %s\n' % (jmp(stmt.condition), else_label)

        code += generate_asm(stmt.true)
        code += ('jmp' + end_label + '\n')

        code += else_label + '\n'
        code += generate_asm(stmt.false)
        code += ('jmp' + end_label + '\n')

        return code
    elif isinstance(stmt, Loop):
        end_label = '.LOOP_END_' + random.randint(0, 9999999)
        loop_label = '.LOOP_' + random.randint(0, 9999999)

        code = 'mov eax, DWORD PTR [rbp-4]\n' \
               'cmp eax, DWORD PTR [rbp-8]\n' \
               '%s %s\n' % (jmp(stmt.condition), end_label)

        code += generate_asm(stmt.true)
        code += ('jmp' + loop_label + '\n')

        return code
    elif isinstance(stmt, WriteString):
        str_label = 'STRING_' + str(random.randint(0, 9999999))

        strings[str_label] = stmt.string.string + '\n'

        return 'mov rax, 1\n' \
               'mov rdi, 1\n' \
               'mov rsi, $%s\n' \
               'mov rdx, %d\n' \
               'syscall\n' % (str_label, len(stmt.string.string) + 1)
    else:
        raise Exception(stmt.__class__)


def generator(ast):
    code = open('src/lib/lib.asm').read()

    for stmt in ast:
        code += generate_asm(stmt) + '\n'

    code += 'mov eax, 1\nmov ebx, 0\nint 0x80\n\n'

    # code += 'section .data\n'
    # code += 'section .data\n'

    for label in strings.keys():
        code += '%s: .string %s\n' % (label, strings[label].strip())

    return code
