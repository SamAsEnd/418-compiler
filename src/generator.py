def generator(tokens):
    code = '#include <stdio.h>\n' \
           '\n' \
           'int main() {\n' \
           '\t'

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
        elif n == 'read':
            code += 'scanf("%d", &' + t[0] + ' );'
        elif n == 'write':
            if t[0].startswith('"'):
                code += 'printf("%s\\n", ' + t[0] + ' );'
            else:
                code += 'printf("%d", ' + t[0] + ' );'
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
