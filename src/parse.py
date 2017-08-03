import re

# keywords
KEYWORD_VAR = '(?:var)'
KEYWORD_IF = '(?:if)'
KEYWORD_ELIF = '(?:elif)'
KEYWORD_DO = '(?:do)'
KEYWORD_WHILE = '(?:while)'
KEYWORD_END = '(?:end)'
KEYWORD_ELSE = '(?:else)'
KEYWORD_WRITE = '(?:write)'
KEYWORD_READ = '(?:read)'

# operators
OP_ASSIGNMENT = '='

OP_GREATER_THAN = '(>)'
OP_LESS_THAN = '(<)'
OP_EQUAL = '(~)'

# complex
NUMBER_LITERAL = '([-]?[1-9]+[0-9]*)'
VARIABLE_IDENTIFIER = '([A-Za-z_]+[A-Za-z_0-9]*)'
STRING_LITERAL = '("[^"]*")'

# complex

VALUE = "(?:(?:%s)|(?:%s))" % (NUMBER_LITERAL, VARIABLE_IDENTIFIER)

OP_ARITHMETIC = "([+\-*/%])"

EXPRESSION = "(?:(?:%s$)|(?:(?:%s)\s*(?:%s)\s*(?:%s)))" % (VALUE, VALUE, OP_ARITHMETIC, VALUE)

ASSIGNMENT = "(?:(?:%s)\s*%s\s*(?:%s))" % (VARIABLE_IDENTIFIER, OP_ASSIGNMENT, EXPRESSION)

VAR_DECLARE = "(?:%s\s*(?:%s)\s*(?:%s\s*(?:%s))?)" \
              % (KEYWORD_VAR, VARIABLE_IDENTIFIER, OP_ASSIGNMENT, EXPRESSION)

GREAT_COND = VALUE + '\s*' + OP_GREATER_THAN + '\s*' + VALUE
LESS_COND = VALUE + '\s*' + OP_LESS_THAN + '\s*' + VALUE
EQUAL_COND = VALUE + '\s*' + OP_EQUAL + '\s*' + VALUE

CONDI = "(?:(?:%s)|(?:%s)|(?:%s))" % (GREAT_COND, LESS_COND, EQUAL_COND)

CON = "(?:%s\s*(?:%s)\s*(?:%s))"

IF_COND = CON % (KEYWORD_IF, CONDI, KEYWORD_DO)
ELIF_COND = CON % (KEYWORD_ELIF, CONDI, KEYWORD_DO)
ELSE_COND = "(?:%s\s*(?:%s))" % (KEYWORD_ELSE, KEYWORD_DO)
END_COND = KEYWORD_END

WHILE_COND = CON % (KEYWORD_WHILE, CONDI, KEYWORD_DO)

WRITE_CMD = "(?:%s\s*(?:(?:%s)|(?:%s)))" % (KEYWORD_WRITE, EXPRESSION, STRING_LITERAL)
READ_CMD = "(?:%s\s*(?:%s))" % (KEYWORD_READ, VARIABLE_IDENTIFIER,)

g = []


def parse(line):
    for rule in [VAR_DECLARE, ASSIGNMENT, IF_COND, ELIF_COND, ELSE_COND, END_COND, READ_CMD, WRITE_CMD]:
        mc = re.match(rule, line)
        if mc is not None:
            tokens = filter(None, mc.groups())
            print line, ' ' * 12, tokens


def read():
    content = open('../sample/code.418', 'r').read()

    com = []

    for line in content.splitlines():
        com.append(parse(line.lstrip().rstrip()))

        # print (com)


read()
