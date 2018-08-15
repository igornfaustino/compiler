import ply.lex as lex

reserved = {
    'se': 'SE',
    'então': 'ENTAO',
    'fim': 'FIM',
    'senão': 'SENAO',
    'repita': 'REPITA',
    'leia': 'LEIA',
    'retorna': 'RETORNA',
    'até': 'ATE',
    'inteiro': 'INTEIRO',
    'flutuante': 'FLUTUANTE',
}

tokens = [
    # NUMBERS (DONE)
    'N_INT',
    'N_FLOAT',

    # NAMES
    'ID',

    # OPERATORS
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQUAL',
    'ASSIGNMENT'

    # SYMBOLS
] + list(reserved.values())

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

# Names
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


# Ply functions
def t_error(t):
    print("Illegal characters '" + t.value + "' at line " +
          str(t.lexer.lineno) + "." + str(t.lexpos))
    exit(1)
    t.lexer.skip(1)
    return t


def t_newline(t):
    r'\n+'
    print(1)
    t.lexer.lineno += len(t.value)


t_ignore = ' \t\r\f\v'


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
