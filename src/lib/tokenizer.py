import re
import sys

LITERAL_NUMBER = '(?:([-]?[1-9]+[0-9]*)|(0))'
LITERAL_STRING = '("[^"]*")'

VARIABLE = '([A-Za-z_]+[A-Za-z_0-9]*)'

OPERATOR_ARITHMETIC = "([+\-*/%]{1})"
OPERATOR_LOGICAL = "(?:([><~]{1})|(?:(>=)|(<=)){1})"

KEYWORD_DO = '(?:do)'
KEYWORD_ELIF = '(?:elif)'
KEYWORD_ELSE = '(?:else)'
KEYWORD_END = '(?:end)'
KEYWORD_IF = '(?:if)'
KEYWORD_READ = '(?:read)'
KEYWORD_VAR = '(?:var)'
KEYWORD_WHILE = '(?:while)'
KEYWORD_WRITE = '(?:write)'
KEYWORD_WRITE_LINE = '(?:writeln)'

VALUE = "(?:(?:%s)|(?:%s))" % (LITERAL_NUMBER, VARIABLE)

CONDITION = "(?:(?:%s)\s*(?:%s)\s*(?:%s))" % (VALUE, OPERATOR_LOGICAL, VALUE)
EXPRESSION = "(?:(?:%s$)|(?:(?:%s)\s*(?:%s)\s*(?:%s)))" % (VALUE, VALUE, OPERATOR_ARITHMETIC, VALUE)

COMMENT_STATEMENT = "[#](.*)"
VAR_DECLARE_STATEMENT = "^(?:%s\s+(?:%s)\s*(?:=\s*(?:%s))?)$" % (KEYWORD_VAR, VARIABLE, EXPRESSION)
ASSIGNMENT_STATEMENT = "^(?:(?:%s)\s*=\s*(?:%s))$" % (VARIABLE, EXPRESSION)

CONDITIONALS = "^(?:%s\s+(?:%s)\s+(?:%s))$"

IF_CONDITION = CONDITIONALS % (KEYWORD_IF, CONDITION, KEYWORD_DO)
ELIF_CONDITION = CONDITIONALS % (KEYWORD_ELIF, CONDITION, KEYWORD_DO)
WHILE_CONDITION = CONDITIONALS % (KEYWORD_WHILE, CONDITION, KEYWORD_DO)

ELSE_CONDITION = "^(?:%s\s+(?:%s))$" % (KEYWORD_ELSE, KEYWORD_DO)
END_CONDITION = "^(?:%s)$" % KEYWORD_END

WRITE_STATEMENT = "^(?:%s\s+(?:(?:%s)|(?:%s)))$" % (KEYWORD_WRITE, EXPRESSION, LITERAL_STRING)
WRITE_LINE_STATEMENT = "^(?:%s\s+(?:(?:%s)|(?:%s)))$" % (KEYWORD_WRITE_LINE, EXPRESSION, LITERAL_STRING)
READ_STATEMENT = "^(?:%s\s+(?:%s))$" % (KEYWORD_READ, VARIABLE,)

statements = [
    ('comment', COMMENT_STATEMENT),

    ('var declare', VAR_DECLARE_STATEMENT),
    ('assignment', ASSIGNMENT_STATEMENT),

    ('if', IF_CONDITION),
    ('elif', ELIF_CONDITION),
    ('else', ELSE_CONDITION),

    ('while', WHILE_CONDITION),

    ('end', END_CONDITION),

    ('write', WRITE_STATEMENT),
    ('writeln', WRITE_LINE_STATEMENT),
    ('read', READ_STATEMENT),
]


def get_token(line, line_number):
    for name, rule in statements:
        mc = re.match(rule, line)
        if mc is not None:
            return name, [token for token in filter(None, mc.groups())]

    raise SyntaxError('on line %d "%s"' % (line_number, line))


def tokenize(content):
    tokens = []
    line_number = 1

    for line in content.splitlines():
        line = line.strip()
        if len(line) > 0:
            tokens.append(get_token(line, line_number))
        line_number += 1

    return tokens
