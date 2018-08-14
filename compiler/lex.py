import ply.lex as lex

tokens = [
    # NUMBERS
    'N_INT',
    'N_FLOAT',

    # TYPES
    'INTEIRO',
    'FLUTUANTE',

    # KEY WORDS
    'SE',
    'ENTAO',
    'FIM',
    'SENAO',
    'REPITA',
    'LEIA',
    'RETORNA'
    'ATE',

    # NAMES
    'NAME',

    # OPERATORS
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',

    # OTHERS
]

# Numbers
def t_N_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_N_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

def t_error(t):
    print("Illegal characters '" + t.value + "' at line " + str(t.lexer.lineno) + "." + str(t.lexpos))
    exit(1)
    t.lexer.skip(1)
    return t

def scan(content):
    lexer = lex.lex()
    lexer.input(content)

    content_tokens = []
    while True:
        tok = lexer.token()
        if not tok or tok.value == 'error':
            break
        content_tokens.append(tok)
    return content_tokens


if __name__ == '__main__':
    pass