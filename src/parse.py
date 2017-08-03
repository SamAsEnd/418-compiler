import os
import re
import sys

KEYWORD_VAR = '(?:var)'
KEYWORD_IF = '(?:if)'
KEYWORD_ELIF = '(?:elif)'
KEYWORD_DO = '(?:do)'
KEYWORD_WHILE = '(?:while)'
KEYWORD_END = '(?:end)'
KEYWORD_ELSE = '(?:else)'
KEYWORD_WRITE = '(?:write)'
KEYWORD_READ = '(?:read)'

NUMBER_LITERAL = '(?:([-]?[1-9]+[0-9]*)|(0))'
VARIABLE_IDENTIFIER = '([A-Za-z_]+[A-Za-z_0-9]*)'
STRING_LITERAL = '("[^"]*")'

VALUE = "(?:(?:%s)|(?:%s))" % (NUMBER_LITERAL, VARIABLE_IDENTIFIER)

OP_ARITHMETIC = "([+\-*/%])"
OP_LOGICAL = "([><~])"

EXPRESSION = "(?:(?:%s$)|(?:(?:%s)\s*(?:%s)\s*(?:%s)))" % (VALUE, VALUE, OP_ARITHMETIC, VALUE)
CONDITION = "(?:(?:%s)\s*(?:%s)\s*(?:%s))" % (VALUE, OP_LOGICAL, VALUE)

ASSIGNMENT_STATEMENT = "^(?:(?:%s)\s*=\s*(?:%s))$" % (VARIABLE_IDENTIFIER, EXPRESSION)

VAR_DECLARE_STATEMENT = "^(?:%s\s*(?:%s)\s*(?:=\s*(?:%s))?)$" % (KEYWORD_VAR, VARIABLE_IDENTIFIER, EXPRESSION)

_C_ = "^(?:%s\s*(?:%s)\s*(?:%s))$"

IF_CONDITION = _C_ % (KEYWORD_IF, CONDITION, KEYWORD_DO)
ELIF_CONDITION = _C_ % (KEYWORD_ELIF, CONDITION, KEYWORD_DO)
ELSE_CONDITION = "^(?:%s\s*(?:%s))$" % (KEYWORD_ELSE, KEYWORD_DO)
END_CONDITION = "^(?:%s)$" % KEYWORD_END

WHILE_CONDITION = _C_ % (KEYWORD_WHILE, CONDITION, KEYWORD_DO)

WRITE_STATEMENT = "^(?:%s\s*(?:(?:%s)|(?:%s)))$" % (KEYWORD_WRITE, EXPRESSION, STRING_LITERAL)
READ_STATEMENT = "^(?:%s\s*(?:%s))$" % (KEYWORD_READ, VARIABLE_IDENTIFIER,)

COMMENT = "^[#](.*)$"
rules = [
    ('var', VAR_DECLARE_STATEMENT),
    ('ass', ASSIGNMENT_STATEMENT),
    ('if', IF_CONDITION),
    ('elif', ELIF_CONDITION),
    ('else', ELSE_CONDITION),
    ('end', END_CONDITION),
    ('while', WHILE_CONDITION),
    ('write', WRITE_STATEMENT),
    ('read', READ_STATEMENT),
    ('com', COMMENT),
]


def generator(tokens):
    code = '#include <stdio.h>\n\nint main() {\n\t'

    for n, t in tokens:
        if n == 'var':
            code += 'int '
            code += t[0]
            if len(t) > 1:
                code += ' = '
                code += ' '.join(t[1:])
            code += ';'
        elif n == 'ass':
            code += t[0]
            if len(t) > 1:
                code += ' '.join(t[1:])
            code += ';'
        elif n == 'ass':
            code += t[0]
            declared_vars.append(t[0])
            if len(t) > 1:
                code += ' '.join(t[1:])
            code += ';'
        elif n == 'read':
            code += 'scanf("%d", &' + t[0] + ' );'
        elif n == 'write':
            if t[0].startswith('"'):
                code += 'printf("%s\\n", ' + t[0] + ' );'
            else:
                code += 'printf("%d\\n", ' + t[0] + ' );'
        elif n == 'while':
            code += 'while (' + (' '.join(t).replace('~', '==')) + ') { '
        elif n == 'if':
            code += 'if (' + (' '.join(t).replace('~', '==')) + ') { '
        elif n == 'elif':
            code += '} else if (' + (' '.join(t).replace('~', '==')) + ') { '
        elif n == 'else':
            code += '} else { '
        elif n == 'end':
            code += '}'
        else:
            pass
        code += '\n\t'

    return code + '\n}'

def parse(line):
    for name, rule in rules:
        mc = re.match(rule, line)
        if mc is not None:
            tokens = filter(None, mc.groups())
            return name, tokens

    sys.stderr.write('Error on line "' + line + '"')
    exit(1)


def read():
    content = open('../sample/code.418', 'r').read()

    tokens = []

    for line in content.splitlines():
        line = line.lstrip().rstrip()
        if len(line) > 0:
            tokens.append(parse(line))

    tokens = filter(None, tokens)
    code = generator(tokens)
    # print code
    open('test.c', 'w').write(code)
    os.system('gcc test.c -o test')
    print 'done'

read()
