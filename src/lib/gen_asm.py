import random

from lib.nodes import *

variables = []

strings = {}


def offset(var: Variable) -> int:
    return (variables.index(var.name) + 1) * -4


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


def val(value: Value) -> str:
    if isinstance(value, Number):
        return '$' + str(value.number)
    else:
        return '%d(%%rbp)' % offset(value)


def generate_asm(stmt: Statement):
    if isinstance(stmt, VarDeclare):
        variables.append(stmt.variable.name)
        return generate_asm(Assignment(stmt.variable, stmt.expression))
    elif isinstance(stmt, Assignment):
        if isinstance(stmt.expression, Number):
            return """
                    movl    %s, %d(%%rbp)
                    """ % (val(stmt.expression), offset(stmt.variable))
        elif isinstance(stmt.expression, Variable):
            return """
                    movl    %s, %%eax
                    movl    %%eax, %d(%%rbp)
                    """ % (val(stmt.expression), offset(stmt.variable))
        elif isinstance(stmt.expression, Addition):
            return """
                    movl    %s, %%eax
                    movl    %s, %%edx
                    addl    %%edx, %%eax
                    movl    %%eax, %d(%%rbp)
                   """ % (
                val(stmt.expression.first_operand),
                val(stmt.expression.second_operand),
                offset(stmt.variable))
        elif isinstance(stmt.expression, Subtraction):
            return """
                    movl    %s, %%eax
                    movl    %s, %%edx
                    subl    %%edx, %%eax
                    movl    %%eax, %d(%%rbp)
                    """ % (
                val(stmt.expression.first_operand),
                val(stmt.expression.second_operand),
                offset(stmt.variable))
        elif isinstance(stmt.expression, Multiplication):
            return """
                    movl    %s, %%eax
                    imull   %s, %%eax
                    movl    %%eax, %d(%%rbp)
                    """ % (
                val(stmt.expression.first_operand),
                val(stmt.expression.second_operand),
                offset(stmt.variable))
        elif isinstance(stmt.expression, Division):
            return """
                    movl    %s, %%eax
                    cltd
                    idivl   %s
                    movl    %%eax, %d(%%rbp)
                    """ % (
                val(stmt.expression.first_operand),
                val(stmt.expression.second_operand),
                offset(stmt.variable))
        elif isinstance(stmt.expression, Modulus):
            return """
                    movl    %s, %%eax
                    cltd
                    idivl   %s
                    movl    %%edx, %d(%%rbp)
                    """ % (
                val(stmt.expression.first_operand),
                val(stmt.expression.second_operand),
                offset(stmt.variable))
    elif isinstance(stmt, Comment):
        return '#' + stmt.string
    elif isinstance(stmt, CompoundStatement):
        code = ''
        for stmt in stmt:
            code += generate_asm(stmt)
        return code
    elif isinstance(stmt, Conditional):
        end_label = '.label_jmp_end_' + str(random.randint(0, 9999999))
        else_label = '.label_jmp_else_' + str(random.randint(0, 9999999))

        code = """
                movl    %s, %%eax
                cmpl    %s, %%eax
                %s      %s
                """ % (
            val(stmt.condition.first_operand),
            val(stmt.condition.second_operand),
            jmp(stmt.condition), else_label)

        code += generate_asm(stmt.true)
        code += ('jmp ' + end_label + '\n')

        code += else_label + ':\n'
        code += generate_asm(stmt.false)
        code += ('jmp ' + end_label + '\n')

        return code + end_label + ':\n'
    elif isinstance(stmt, Loop):
        end_label = '.label_loop_end_' + str(random.randint(0, 9999999))
        loop_label = '.label_loop_' + str(random.randint(0, 9999999))

        code = loop_label + ':\n'

        code += """
                movl    %s, %%eax
                cmpl    %s, %%eax
                %s      %s
                """ % (
            val(stmt.condition.first_operand), val(stmt.condition.second_operand),
            jmp(stmt.condition), end_label)

        code += generate_asm(stmt.true)
        code += ('jmp ' + loop_label + '\n')

        return code + end_label + ':\n'
    elif isinstance(stmt, WriteString):
        str_label = '.string_' + str(random.randint(0, 9999999))

        strings[str_label] = stmt.string.string + '\n'

        return """
                mov     $1, %%rax
                mov     $1, %%rdi
                mov     $%s, %%rsi
                mov     $%d, %%rdx
                syscall
               """ % (
            str_label, len(stmt.string.string) - 2)
    elif isinstance(stmt, WriteValue):
        return """
                mov     %s, %%rax
                mov     %%rax, %%rdi
                mov     $0, %%rax
                call writeNumber

                mov     %%rax, %%rdx
                mov     $1, %%rax
                mov     $1, %%rdi
                mov     $str, %%rsi
                syscall
               """ % val(stmt.variable)
    elif isinstance(stmt, Read):
        return """
                mov     $0, %%rax
                mov     $0, %%rdi
                mov     $str, %%rsi
                mov     $12, %%rdx
                syscall

                call readNumber

                mov     %%rax, %d(%%rbp)
               """ % offset(stmt.variable)
    else:
        raise Exception(stmt.__class__)


def generator(ast):
    code = """
.section    .bss

.section     .text
        .globl  main
        .type   main, @function

_start:
main:
    movq    %rsp, %rbp
"""

    for stmt in ast:
        code += generate_asm(stmt) + '\n'

    code += """
                mov     $60, %rax
                mov     $0, %rdi
                syscall
            """

    for label in strings.keys():
        code += '%s: .string %s\n' % (label, strings[label])

    return code
