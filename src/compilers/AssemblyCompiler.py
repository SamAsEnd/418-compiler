import os
import tempfile

from compilers.Compiler import Compiler
from nodes import *


class AssemblyCompiler(Compiler):
    # start from 100,000
    counter = 100000

    def __init__(self, tree: CompoundStatement) -> None:
        super().__init__(tree)

        # holds the declared variables
        self.variables = []

        # holds the static string found in the program
        self.strings = {}

        self.code = ''

    def __str__(self):
        return self.code

    def get_tail(self) -> str:
        """
        Return a consecutive integer as a  string 
        to be appended by ladles in the asm
        :return: str
        """
        self.counter += 1
        return str(self.counter)

    def offset(self, var: Variable) -> int:
        """
        return the variable offset of a variable in the stack
        :param var: the variable
        :return: the variable offset from the base pointer
        """
        return (self.variables.index(var.name) + 1) * -4

    @staticmethod
    def jump(condition: Condition) -> str:
        """
        Return the inverse of the condition node
        eg: passing GreaterThan(>) with return LessOrEqual (<=) 
        :param condition: 
        :return: the inverse of the condition node
        """
        if isinstance(condition, EqualTo):
            return 'jne'  # NotEqualTo
        elif isinstance(condition, GreaterThan):
            return 'jle'  # LessOrEqualTo
        elif isinstance(condition, GreaterOrEqualTo):
            return 'jl'  # LessThan
        elif isinstance(condition, LessThan):
            return 'jge'  # GreaterOrEqualTo
        elif isinstance(condition, LessOrEqualTo):
            return 'jg'  # GreaterThan
        else:
            return 'je'  # EqualTo

    def val(self, value: Value) -> str:
        """
        Return a dollar sign followed by the number if the value is a Number
        else return a rbp offset of the give variable
        :param value: a value
        :return: asm literal number or stack variable reference
        """
        if isinstance(value, Number):
            # $ is prepended in At&t assembly syntax used by GNU as
            return '$' + str(value.number)
        else:
            # rbp is a 64 register equivalent of ebp in 32 bit processor
            # -4(%rbp) is equivalent with rbp-4 in intel syntax
            return '%d(%%rbp)' % self.offset(value)

    def compile_statement(self, stmt: Statement) -> str:
        """
        Compile the passed to an assembly code
        :param stmt: the abstract syntax tree node
        :return: the assembly code as a string
        """
        if isinstance(stmt, VarDeclare):
            # append the variable name to the variables list
            self.variables.append(stmt.variable.name)
            # processed as a assignment statement
            return self.compile_statement(Assignment(stmt.variable, stmt.expression))

        elif isinstance(stmt, Assignment):
            # Assignment Statement
            if isinstance(stmt.expression, Number):
                # move the number to the given variable
                return """
                        movl    %s, %d(%%rbp)
                        """ % (self.val(stmt.expression), self.offset(stmt.variable))

            elif isinstance(stmt.expression, Variable):
                # move the variable value to the ax register
                # then mov it to the other variable
                # bcoz we cant move content from memory to memory
                return """
                        movl    %d(%%rbp), %%eax
                        movl    %%eax, %d(%%rbp)
                        """ % (self.offset(stmt.expression), self.offset(stmt.variable))

            elif isinstance(stmt.expression, Addition):
                # move the two operands to ax and dx
                # add them on ax
                # store the result in the variable
                return """
                        movl    %s, %%eax
                        movl    %s, %%edx
                        addl    %%edx, %%eax
                        movl    %%eax, %d(%%rbp)
                       """ % (
                    self.val(stmt.expression.first_operand),
                    self.val(stmt.expression.second_operand),
                    self.offset(stmt.variable))

            elif isinstance(stmt.expression, Subtraction):
                # move the two operands to ax and dx respectively
                # subtract dx from ax
                # store the result in the variable
                return """
                        movl    %s, %%eax
                        movl    %s, %%edx
                        subl    %%edx, %%eax
                        movl    %%eax, %d(%%rbp)
                        """ % (
                    self.val(stmt.expression.first_operand),
                    self.val(stmt.expression.second_operand),
                    self.offset(stmt.variable))

            elif isinstance(stmt.expression, Multiplication):
                # move the two operands to ax and dx
                # multiply them on ax
                # store the result in the variable
                return """
                        movl    %s, %%eax
                        imull   %s, %%eax
                        movl    %%eax, %d(%%rbp)
                        """ % (
                    self.val(stmt.expression.first_operand),
                    self.val(stmt.expression.second_operand),
                    self.offset(stmt.variable))

            elif isinstance(stmt.expression, Division):
                # move the first operand to ax
                # sign-extends (stretch) eax into edx:eax extend
                # divide the edx:eax by the value
                # store the quotient at eax in the variable
                return """
                        movl    %s, %%eax
                        cltd
                        idivl   %s
                        movl    %%eax, %d(%%rbp)
                        """ % (
                    self.val(stmt.expression.first_operand),
                    self.val(stmt.expression.second_operand),
                    self.offset(stmt.variable))

            elif isinstance(stmt.expression, Modulus):
                # move the first operand to ax
                # sign-extends (stretch) eax into edx:eax extend
                # divide the edx:eax by the value
                # store the reminder at edx in the variable
                return """
                        movl    %s, %%eax
                        cltd
                        idivl   %s
                        movl    %%edx, %d(%%rbp)
                        """ % (
                    self.val(stmt.expression.first_operand),
                    self.val(stmt.expression.second_operand),
                    self.offset(stmt.variable))

            else:
                raise SyntaxError(stmt.expression.__class__ + ' not implemented')

        elif isinstance(stmt, Comment):
            # pass the comment too :)
            return '#' + stmt.string

        elif isinstance(stmt, CompoundStatement):
            # just iterate and recurse
            code = ''

            for stmt in stmt:
                code += self.compile_statement(stmt)

            return code

        elif isinstance(stmt, Conditional):
            # where the program branches

            # the last label at the end of the condition
            end_label = '.label_jmp_end_' + self.get_tail()
            # the other branch we need to jump if the condition fails
            else_label = '.label_jmp_else_' + self.get_tail()

            # move the first value to the ax register
            # compare with the second value
            # if it DOESN'T match jmp to the else condition
            code = """
                    movl    %s, %%eax
                    cmpl    %s, %%eax
                    %s      %s
                    """ % (
                self.val(stmt.condition.first_operand),
                self.val(stmt.condition.second_operand),
                self.jump(stmt.condition), else_label)

            # recurse to the "true" option
            code += self.compile_statement(stmt.true)
            # jump to the end label when we r done with the "true" option
            code += ('jmp ' + end_label + '\n')

            # start the else branch
            code += else_label + ':\n'
            # recurse to the "false" option
            code += self.compile_statement(stmt.false)
            # jump to the end label
            code += ('jmp ' + end_label + '\n')

            # mark the end label
            code += end_label + ':\n'

            return code

        elif isinstance(stmt, Loop):
            # where the program iterates

            # the last label at the end of the loop
            end_label = '.label_loop_end_' + self.get_tail()
            # the start of the loop
            loop_label = '.label_loop_' + self.get_tail()

            # mark the start of the loop
            code = loop_label + ':\n'

            # move the first value to the ax register
            # compare with the second value
            # if it DOESN'T match jmp to the end of the loop
            code += """
                    movl    %s, %%eax
                    cmpl    %s, %%eax
                    %s      %s
                    """ % (
                self.val(stmt.condition.first_operand),
                self.val(stmt.condition.second_operand),
                self.jump(stmt.condition), end_label)

            # recurse to the loop body
            code += self.compile_statement(stmt.true)
            # jump to the start of the loop unconditionally
            code += ('jmp ' + loop_label + '\n')

            # mark the end label
            code += end_label + ':\n'

            return code

        elif isinstance(stmt, WriteString):
            # the label for the string
            str_label = 'string_' + self.get_tail()

            # add to the list of strings
            self.strings[str_label] = stmt.string.string + '\n'

            # call the system write interrupt
            # 1     write   sys_write
            # sys_write(unsigned int fd, const char *buf, size_t count)
            return """
                    mov     $1, %%rax
                    mov     $1, %%rdi
                    mov     $%s, %%rsi
                    mov     $%d, %%rdx
                    syscall
                   """ % (
                str_label, len(stmt.string.string) - 2)

        elif isinstance(stmt, WriteValue):
            # move the variable to di through ax register
            # call write number
            # invoke the syscall
            # 1     write   sys_write
            # sys_write(unsigned int fd, const char *buf, size_t count)
            return """
                    mov     %s, %%rax
                    mov     %%rax, %%rdi
                    mov     $0, %%rax
                    call writeNumber
    
                    mov     %%rax, %%rdx
                    mov     $1, %%rax
                    mov     $1, %%rdi
                    mov     $buffer, %%rsi
                    syscall
                   """ % self.val(stmt.variable)

        elif isinstance(stmt, Read):
            # invoke the syscall
            # 0	read	sys_read
            # sys_write(unsigned int fd, char *buf, size_t count)
            # call readNumber
            # store the result in the variable
            return """
                    mov     $0, %%rax
                    mov     $0, %%rdi
                    mov     $buffer, %%rsi
                    mov     $12, %%rdx
                    syscall
    
                    call readNumber
    
                    mov     %%eax, %d(%%rbp)
                   """ % self.offset(stmt.variable)

        else:
            raise Exception(stmt.__class__)

    def compile(self):
        # append the std
        code = """
                .globl      main
                .type       main, @function
                
                .section    .text
                main:
                    movq    %rsp, %rbp
                    :418-main-stack:
                """

        for stmt in self.tree:
            code += self.compile_statement(stmt) + '\n'

        code += """
                    mov     $60, %rax
                    mov     $0, %rdi
                    syscall
                """

        for label in self.strings.keys():
            code += '%s: .string %s\n' % (label, self.strings[label])

        code = code.replace(':418-main-stack:', 'sub $%d, %%rsp' % (((len(self.variables) - 1) // 4 + 1) * 16))

        self.code = code

    def build(self, args):
        if not args.asm:
            asm_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.s')
        else:
            asm_file = open(args.output+'.s', 'w')

        asm_file.write(self.code)
        asm_file.close()

        if args.output is not None:
            # assemble the asm
            status = os.system('as -g %s -o %s' % (asm_file.name, args.output + '.o'))

            if status != 0:
                raise RuntimeError('as: assembler failed with exit code ' + str(status))

            # link the output
            status = os.system('ld -o %s %s lib/lib418.o' % (args.output, args.output + '.o'))

            if status != 0:
                raise RuntimeError('ld: linker failed with exit code ' + str(status))

            # noinspection PyBroadException
            try:
                os.unlink(args.output + '.o')
            except:
                pass
