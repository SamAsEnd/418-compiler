import re
from pprint import pprint

KEYWORD_VAR = '(?:var)'
KEYWORD_IF = '(?:if)'
KEYWORD_ELIF = '(?:elif)'
KEYWORD_DO = '(?:do)'
KEYWORD_WHILE = '(?:while)'
KEYWORD_END = '(?:end)'
KEYWORD_ELSE = '(?:else)'
KEYWORD_WRITE = '(?:write)'
KEYWORD_READ = '(?:read)'

NUMBER_LITERAL = '([-]?[1-9]+[0-9]*)'
VARIABLE_IDENTIFIER = '([A-Za-z_]+[A-Za-z_0-9]*)'
STRING_LITERAL = '("[^"]*")'

VALUE = "(?:(?:%s)|(?:%s))" % (NUMBER_LITERAL, VARIABLE_IDENTIFIER)

OP_ARITHMETIC = "([+\-*/%])"
OP_LOGICAL = "([><~])"

EXPRESSION = "(?:(?:%s$)|(?:(?:%s)\s*(?:%s)\s*(?:%s)))" % (VALUE, VALUE, OP_ARITHMETIC, VALUE)
CONDITION = "(?:(?:%s)\s*(?:%s)\s*(?:%s))" % (VALUE, OP_LOGICAL, VALUE)

ASSIGNMENT_STATEMENT = "(?:(?:%s)\s*=\s*(?:%s))" % (VARIABLE_IDENTIFIER, EXPRESSION)

VAR_DECLARE_STATEMENT = "(?:%s\s*(?:%s)\s*(?:=\s*(?:%s))?)" % (KEYWORD_VAR, VARIABLE_IDENTIFIER, EXPRESSION)

IF_CONDITION = "^(?:%s\s*(?:%s)\s*(?:%s))$" % (KEYWORD_IF, CONDITION, KEYWORD_DO)
ELIF_CONDITION = "^(?:%s\s*(?:%s)\s*(?:%s))$" % (KEYWORD_ELIF, CONDITION, KEYWORD_DO)
ELSE_CONDITION = "^(?:%s\s*(?:%s))$" % (KEYWORD_ELSE, KEYWORD_DO)
END_CONDITION = "^(?:%s)$" % KEYWORD_END

WHILE_CONDITION = "^(?:%s\s*(?:%s)\s*(?:%s))$" % (KEYWORD_WHILE, CONDITION, KEYWORD_DO)

WRITE_STATEMENT = "(?:%s\s*(?:(?:%s)|(?:%s)))" % (KEYWORD_WRITE, EXPRESSION, STRING_LITERAL)
READ_STATEMENT = "(?:%s\s*(?:%s))" % (KEYWORD_READ, VARIABLE_IDENTIFIER,)
COMMENT = "[#].*"

rules = [
    ('var', VAR_DECLARE_STATEMENT),
    ('ass', ASSIGNMENT_STATEMENT),
    ('if', IF_CONDITION),
    ('elif', ELIF_CONDITION),
    ('else', ELSE_CONDITION),
    ('end', END_CONDITION),
    ('write', WRITE_STATEMENT),
    ('read', READ_STATEMENT),
    ('com', COMMENT),
]


def parse(line):
    for name, rule in rules:
        mc = re.match(rule, line)
        if mc is not None:
            tokens = filter(None, mc.groups())
            return name, tokens


def read():
    content = open('../sample/code.418', 'r').read()

    com = []

    for line in content.splitlines():
        com.append(parse(line.lstrip().rstrip()))

    com = filter(None, com)
    pprint(com)

read()
