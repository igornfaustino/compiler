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
    'NOT_EQUAL',
    'GREATER_THAN',
    'GREATER_EQUAL',
    'LESS_THAN',
    'LESS_EQUAL',
    'ASSIGNMENT',
    # Logical
    'AND',
    'OR',

    # SYMBOLS
    'COLON',
    'COMMA',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',

    # OTHERS
    'COMMENT',
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
t_EQUAL = r'\='
t_NOT_EQUAL = r'<>'
t_GREATER_THAN = r'>'
t_GREATER_EQUAL = r'>='
t_LESS_THAN = r'<'
t_LESS_EQUAL = r'<='
t_ASSIGNMENT = r':='
# LOGICAL
t_AND = r'&&'
t_OR = r'\|\|'


# Symbols
t_COLON = r':'
t_COMMA = r','
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'


# Names
def t_ID(t):
    r'''[a-zA-Z_áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]
    [a-zA-Z_0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*'''
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


# Comments
def t_ignore_COMMENT(t):
    r'({(.|\n)*?(}|$))'
    t.lexer.lineno += t.value.count('\n')


# AUX Functions
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# PLY functions
def t_error(t):
    print("Illegal characters '" + t.value[0] + "' at line " +
          str(t.lexer.lineno) + "." + str(find_column(t.lexer.lexdata, t)))
    exit(1)


def t_newline(t):
    r'\n+'
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
