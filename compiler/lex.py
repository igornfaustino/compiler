import ply.lex as lex
from colorpy import warning, error

# Declare the state
states = (
    ('comment', 'exclusive'),
)

# Declare reserved words
reserved = {
    'se': 'SE',
    'então': 'ENTAO',
    'fim': 'FIM',
    'senão': 'SENAO',
    'repita': 'REPITA',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'retorna': 'RETORNA',
    'até': 'ATE',
    'inteiro': 'INTEIRO',
    'flutuante': 'FLUTUANTE',
}

# Declare tokens
tokens = [
    # NUMBERS
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
    'NOT',

    # SYMBOLS
    'COLON',
    'COMMA',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',

    # 'COMMENT',
] + list(reserved.values())


# Numbers
def t_N_FLOAT(t):
    r'(\d+(\.\d*)?[eE][-+]?\d+)|(\d+\.\d*)'
    t.value = float(t.value)
    return t


def t_N_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Operators
def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'\-'
    return t

def t_MULTIPLY(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'\/'
    return t

def t_EQUAL(t):
    r'\='
    return t

def t_NOT_EQUAL(t):
    r'<>'
    return t

def t_GREATER_EQUAL(t):
    r'>='
    return t

def t_GREATER_THAN(t):
    r'>'
    return t

def t_LESS_EQUAL(t):
    r'<='
    return t

def t_LESS_THAN(t):
    r'<'
    return t

def t_ASSIGNMENT(t):
    r':='
    return t

# LOGICAL
def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NOT(T):
    r'\!'
    return t


# Symbols
def t_COLON(t):
    r':'
    return t

def t_COMMA(t):
    r','
    return t

def t_OPEN_PARENTHESIS(t):
    r'\('
    return t

def t_CLOSE_PARENTHESIS(t):
    r'\)'
    return t

def t_OPEN_BRACKET(t):
    r'\['
    return t

def t_CLOSE_BRACKET(t):
    r'\]'
    return t


# Names
def t_ID(t):
    r'''[a-zA-Z_áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]
    [a-zA-Z_0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*'''
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


# Comments State
# BEGINS HERE

# Match the first {. Enter comment state.
def t_comment(t):
    r'\{'
    # Record the starting position
    t.lexer.code_start = find_column(t)
    t.lexer.comment_line = t.lexer.lineno      # Record the starting line
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('comment')                     # Enter 'comment' state


# Rules for the comment state
def t_comment_lbrace(t):
    r'\{'
    t.lexer.level += 1


def t_comment_rbrace(t):
    r'\}'
    t.lexer.level -= 1

    # If closing brace, return the code fragment
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')


def t_comment_eof(t):
    warning('Comment not closed at position ' + str(
        t.lexer.comment_line) + '.' + str(t.lexer.code_start))
    return None


def t_comment_COMMENT(t):
    r'(.)'
# ENDS HERE


# AUX Functions
def find_column(token):
    input = token.lexer.lexdata
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# PLY functions
def t_ANY_error(t):
    error("Illegal characters '" + t.value[0] + "' at line " +
          str(t.lexer.lineno) + "." + str(find_column(t)))
    exit(1)


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ANY_ignore = ' \t\r\f\v'


lexer = lex.lex()


def scan(content):
    global lexer

    lexer.input(content)

    content_tokens = []
    while True:
        tok = lexer.token()
        if not tok or tok.value == 'error':
            break
        tok.lexpos = find_column(tok)
        content_tokens.append(tok)
    lexer = lex.lex()
    return content_tokens


if __name__ == '__main__':
    pass
