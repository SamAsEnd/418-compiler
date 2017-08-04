import re
import sys

LITERAL_NUMBER = '(?:([-]?[1-9]+[0-9]*)|(0))'
LITERAL_STRING = '("[^"]*")'

VARIABLE = '([A-Za-z_]+[A-Za-z_0-9]*)'

OPERATOR_ARITHMETIC = "([+\-*/%]{1})"
OPERATOR_LOGICAL = "([><~(?:>=)(?:<=)]{1})"

KEYWORD_DO = '(?:do)'
KEYWORD_ELIF = '(?:elif)'
KEYWORD_ELSE = '(?:else)'
KEYWORD_END = '(?:end)'
KEYWORD_IF = '(?:if)'
KEYWORD_READ = '(?:read)'
KEYWORD_VAR = '(?:var)'
KEYWORD_WHILE = '(?:while)'
KEYWORD_WRITE = '(?:write)'

VALUE = "(?:(?:%s)|(?:%s))" % (LITERAL_NUMBER, VARIABLE)

CONDITION = "(?:(?:%s)\s*(?:%s)\s*(?:%s))" % (VALUE, OPERATOR_LOGICAL, VALUE)
EXPRESSION = "(?:(?:%s$)|(?:(?:%s)\s*(?:%s)\s*(?:%s)))" % (VALUE, VALUE, OPERATOR_ARITHMETIC, VALUE)

COMMENT = "^[#](.*)$"
VAR_DECLARE_STATEMENT = "^(?:%s\s*(?:%s)\s*(?:=\s*(?:%s))?)$" % (KEYWORD_VAR, VARIABLE, EXPRESSION)
ASSIGNMENT_STATEMENT = "^(?:(?:%s)\s*=\s*(?:%s))$" % (VARIABLE, EXPRESSION)

CONDITIONALS = "^(?:%s\s*(?:%s)\s*(?:%s))$"

IF_CONDITION = CONDITIONALS % (KEYWORD_IF, CONDITION, KEYWORD_DO)
ELIF_CONDITION = CONDITIONALS % (KEYWORD_ELIF, CONDITION, KEYWORD_DO)
WHILE_CONDITION = CONDITIONALS % (KEYWORD_WHILE, CONDITION, KEYWORD_DO)

ELSE_CONDITION = "^(?:%s\s*(?:%s))$" % (KEYWORD_ELSE, KEYWORD_DO)
END_CONDITION = "^(?:%s)$" % KEYWORD_END

WRITE_STATEMENT = "^(?:%s\s*(?:(?:%s)|(?:%s)))$" % (KEYWORD_WRITE, EXPRESSION, LITERAL_STRING)
READ_STATEMENT = "^(?:%s\s*(?:%s))$" % (KEYWORD_READ, VARIABLE,)

statements = [
    ('comment', COMMENT),

    ('var declare', VAR_DECLARE_STATEMENT),
    ('assignment', ASSIGNMENT_STATEMENT),

    ('if', IF_CONDITION),
    ('elif', ELIF_CONDITION),
    ('else', ELSE_CONDITION),

    ('while', WHILE_CONDITION),

    ('end', END_CONDITION),

    ('write', WRITE_STATEMENT),
    ('read', READ_STATEMENT),
]


def tokenize(line):
    for name, rule in statements:
        mc = re.match(rule, line)
        if mc is not None:
            return name, [token for token in filter(None, mc.groups())]

    sys.stderr.write('Syntax Error: on line "' + line + '"')
    exit(1)
