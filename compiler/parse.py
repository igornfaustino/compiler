import ply.yacc as yacc
from anytree import Node
from lex import tokens, find_column
from colorpy import warning, error
import logging

num = 0
success = True

precedence = (
    ("nonassoc", "ID"),
    ("nonassoc", "OPEN_PARENTHESIS"),
)


def p_program(p):
    '''
    program : declaration_list
    '''

    global num
    root = Node(str(num), value='program')
    num += 1
    p[1].parent = root

    p[0] = root


def p_declaration_list(p):
    '''
    declaration_list : declaration_list declaration
                     | declaration
    '''

    global num
    father = Node(str(num), value='declaration_list')
    num += 1
    if (len(p) == 3):
        p[1].parent = father
        p[2].parent = father
    else:
        p[1].parent = father

    p[0] = father


def p_declaration(p):
    '''
    declaration : var_declaration
                | var_init
                | func_declaration
    '''

    global num
    father = Node(str(num), value='declaration')
    num += 1
    p[1].parent = father
    p[0] = father


def p_var_declaration(p):
    '''
    var_declaration : type COLON var_list
    '''

    global num
    father = Node(str(num), value='var_declaration')
    num += 1
    p[1].parent = father
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father
    p[0] = father


def p_var_init(p):
    '''
    var_init : assignment
    '''

    global num
    father = Node(str(num), value='var_init')
    num += 1
    p[1].parent = father
    p[0] = father


def p_index(p):
    '''
    index : index OPEN_BRACKET expression CLOSE_BRACKET
          | OPEN_BRACKET expression CLOSE_BRACKET
    '''

    global num
    father = Node(str(num), value='index')
    num += 1
    if(len(p) == 5):
        p[1].parent = father
        Node(str(num), father, value=str(
            p[2]), line=p.lineno(2), pos=p.lexpos(2))
        num += 1
        p[3].parent = father
        Node(str(num), father, value=str(
            p[4]), line=p.lineno(4), pos=p.lexpos(4))
        num += 1
    else:
        Node(str(num), father, value=str(
            p[1]), line=p.lineno(1), pos=p.lexpos(1))
        num += 1
        p[2].parent = father
        Node(str(num), father, value=str(
            p[3]), line=p.lineno(3), pos=p.lexpos(3))
        num += 1
    p[0] = father


def p_type(p):
    '''
    type : INTEIRO
         | FLUTUANTE
    '''

    global num
    father = Node(str(num), value="type")
    num += 1
    Node(str(num), value=str(p[1]), parent=father,
         line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    p[0] = father


def p_func_declaration(p):
    '''
    func_declaration : type header
                    | header
    '''

    global num
    father = Node(str(num), value="func_declaration")
    num += 1
    p[1].parent = father
    if(len(p) == 3):
        p[2].parent = father
    p[0] = father


def p_header(p):
    '''
    header : ID OPEN_PARENTHESIS params_list CLOSE_PARENTHESIS body FIM
    '''

    global num
    father = Node(str(num), value="header")
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father
    Node(str(num), father, value=str(p[4]), line=p.lineno(4), pos=p.lexpos(4))
    num += 1
    p[5].parent = father
    Node(str(num), father, value=str(p[6]), line=p.lineno(6), pos=p.lexpos(6))
    num += 1

    p[0] = father


def p_var_list(p):
    '''
    var_list : var_list COMMA var
             | var
    '''

    global num
    father = Node(str(num), value='var_list')
    num += 1
    if(len(p) == 4):
        p[1].parent = father
        Node(str(num), father, value=str(
            p[2]), line=p.lineno(2), pos=p.lexpos(2))
        num += 1
        p[3].parent = father
    else:
        p[1].parent = father

    p[0] = father


def p_var(p):
    '''
    var : ID
        | ID index
    '''

    global num
    father = Node(str(num), value='var', line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    if(len(p) == 3):
        p[2].parent = father
    p[0] = father


def p_params_list(p):
    '''
    params_list : params_list COMMA param
                | param
                | empty
    '''

    global num
    father = Node(str(num), value="params_list")
    num += 1
    if(len(p) == 4):
        p[1].parent = father
        Node(str(num), father, value=str(
            p[2]), line=p.lineno(2), pos=p.lexpos(2))
        num += 1
        p[3].parent = father
    elif(p[1] is not None):
        p[1].parent = father
    else:
        Node(str(num), father, value="")
        num += 1

    p[0] = father


def p_param(p):
    '''
    param : type COLON ID
          | param OPEN_BRACKET CLOSE_BRACKET
    '''

    global num
    father = Node(str(num), value="param")
    num += 1
    p[1].parent = father
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    Node(str(num), father, value=str(p[3]), line=p.lineno(3), pos=p.lexpos(3))
    num += 1
    p[0] = father


def p_body(p):
    '''
    body : body action
         | empty
    '''

    global num
    father = Node(str(num), value="body")
    num += 1
    if(len(p) == 3):
        p[1].parent = father
        p[2].parent = father
    else:
        Node(str(num), father, value="")
        num += 1
    p[0] = father


def p_action(p):
    '''
    action : expression
           | var_declaration
           | se
           | repita
           | leia
           | escreva
           | retorna
    '''

    global num
    father = Node(str(num), value="action")
    num += 1
    p[1].parent = father
    p[0] = father


def p_se(p):
    '''
    se : SE expression ENTAO body FIM
       | SE expression ENTAO body SENAO body FIM
    '''

    global num
    father = Node(str(num), value="conditional")
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    p[2].parent = father
    Node(str(num), father, value=str(p[3]), line=p.lineno(3), pos=p.lexpos(3))
    num += 1
    p[4].parent = father
    Node(str(num), father, value=str(p[5]), line=p.lineno(5), pos=p.lexpos(5))
    num += 1
    if(len(p) == 8):
        p[6].parent = father
        Node(str(num), father, value=str(
            p[7]), line=p.lineno(7), pos=p.lexpos(7))
        num += 1

    p[0] = father


def p_repita(p):
    '''
    repita : REPITA body ATE expression
    '''

    global num
    father = Node(str(num), value="repita")
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    p[2].parent = father
    Node(str(num), father, value=str(p[3]), line=p.lineno(3), pos=p.lexpos(3))
    num += 1
    p[4].parent = father

    p[0] = father


def p_assignment(p):
    '''
    assignment : var ASSIGNMENT expression
    '''

    global num
    father = Node(str(num), value="assignment",
                  line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[1].parent = father
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father

    p[0] = father


def p_leia(p):
    '''
    leia : LEIA OPEN_PARENTHESIS var CLOSE_PARENTHESIS
    '''

    global num
    father = Node(str(num), value="leia")
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father
    Node(str(num), father, value=str(p[4]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    p[0] = father


def p_escreva(p):
    '''
    escreva : ESCREVA OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
    '''

    global num
    father = Node(str(num), value="escreva")
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father
    Node(str(num), father, value=str(p[4]), line=p.lineno(4), pos=p.lexpos(4))
    num += 1

    p[0] = father


def p_retorna(p):
    '''
    retorna : RETORNA OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
    '''

    global num
    father = Node(str(num), value="retorna", line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father
    Node(str(num), father, value=str(p[4]), line=p.lineno(4), pos=p.lexpos(4))
    num += 1

    p[0] = father


def p_expression(p):
    '''
    expression : logic_expression
               | assignment
    '''

    global num
    father = Node(str(num), value="expression")
    num += 1
    p[1].parent = father

    p[0] = father


def p_logic_expression(p):
    '''
    logic_expression : simple_expression
                     | logic_expression logic_operator simple_expression
    '''

    global num
    father = Node(str(num), value="logic_expression")
    num += 1
    p[1].parent = father
    if(len(p) == 4):
        p[2].parent = father
        p[3].parent = father

    p[0] = father


def p_simple_expression(p):
    '''
    simple_expression : additive_expression
                      | simple_expression operator_relational additive_expression
    '''

    global num
    father = Node(str(num), value="simple_expression")
    num += 1
    p[1].parent = father
    if(len(p) == 4):
        p[2].parent = father
        p[3].parent = father

    p[0] = father


def p_additive_expression(p):
    '''
    additive_expression : multiply_expression
                        | additive_expression sum_operator multiply_expression
    '''

    global num
    father = Node(str(num), value="additive_expression")
    num += 1
    p[1].parent = father
    if(len(p) == 4):
        p[2].parent = father
        p[3].parent = father

    p[0] = father


def p_multiply_expression(p):
    '''
    multiply_expression : single_expression
                        | multiply_expression multiply_operator single_expression
    '''

    global num
    father = Node(str(num), value="multiply_expression")
    num += 1
    p[1].parent = father
    if(len(p) == 4):
        p[2].parent = father
        p[3].parent = father

    p[0] = father


def p_single_expression(p):
    '''
    single_expression : factor
                      | sum_operator factor
                      | NOT factor
    '''

    global num
    father = Node(str(num), value="single_expression")
    num += 1
    if (len(p) == 3):
        if(p[1] == '!'):
            Node(str(num), father, value=str(
                p[1]), line=p.lineno(1), pos=p.lexpos(1))
            num += 1
        else:
            p[1].parent = father
        p[2].parent = father
    else:
        p[1].parent = father

    p[0] = father


def p_operator_relational(p):
    '''
    operator_relational : EQUAL
                        | NOT_EQUAL
                        | GREATER_THAN
                        | GREATER_EQUAL
                        | LESS_THAN
                        | LESS_EQUAL
    '''

    global num
    father = Node(str(num), value='relational_op')
    num += 1
    son = Node(str(num), father, value=str(
        p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    p[0] = father


def p_sum_operator(p):
    '''
    sum_operator : PLUS
                 | MINUS
    '''

    global num
    father = Node(str(num), value='sum_operator')
    num += 1
    son = Node(str(num), father, value=str(
        p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    p[0] = father


def p_logic_operator(p):
    '''
    logic_operator : AND
                   | OR
    '''

    global num
    father = Node(str(num), value='logic_op')
    num += 1
    son = Node(str(num), father, value=str(
        p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    p[0] = father


def p_multiply_operator(p):
    '''
    multiply_operator : MULTIPLY
                      | DIVIDE
    '''

    global num
    father = Node(str(num), value='multiply_operator')
    num += 1
    son = Node(str(num), father, value=str(
        p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    p[0] = father


def p_factor(p):
    '''
    factor : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS
           | function_call
           | var
           | num
    '''

    global num
    father = Node(str(num), value='factor')
    num += 1
    if (len(p) == 4):
        Node(str(num), father, value=str(
            p[1]), line=p.lineno(1), pos=p.lexpos(1))
        num += 1
        p[2].parent = father
        Node(str(num), father, value=str(
            p[3]), line=p.lineno(3), pos=p.lexpos(3))
        num += 1
    else:
        p[1].parent = father

    p[0] = father


def p_num(p):
    '''
    num : N_INT
        | N_FLOAT
    '''

    global num
    father = Node(str(num), value='num')
    num += 1
    son = Node(str(num), father, value=p[1], line=p.lineno(1), pos=p.lexpos(1))
    num += 1

    p[0] = father


def p_function_call(p):
    '''
    function_call : ID OPEN_PARENTHESIS arguments_list CLOSE_PARENTHESIS
    '''

    global num
    father = Node(str(num), value='function_call',
                  line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[1]), line=p.lineno(1), pos=p.lexpos(1))
    num += 1
    Node(str(num), father, value=str(p[2]), line=p.lineno(2), pos=p.lexpos(2))
    num += 1
    p[3].parent = father
    Node(str(num), father, value=str(p[4]), line=p.lineno(4), pos=p.lexpos(4))
    num += 1

    p[0] = father


def p_arguments_list(p):
    '''
    arguments_list : arguments_list COMMA expression
                   | expression
                   | empty
    '''

    global num
    father = Node(str(num), value='arguments_list')
    num += 1
    if(len(p) == 4):
        p[1].parent = father
        Node(str(num), father, value=str(
            p[2]), line=p.lineno(2), pos=p.lexpos(2))
        num += 1
        p[3].parent = father
    elif(p[1] is not None):
        p[1].parent = father
    else:
        Node(str(num), father, value="")
        num += 1

    p[0] = father


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    global success
    success = False
    if not p:
        return
    error("Syntax error '" + str(p.value) + "' at line " +
          str(p.lineno) + "." + str(find_column(p)))
    parser.errok()


logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

parser = yacc.yacc()


def parse(content, debug=False):
    result = parser.parse(content, debug=debug)

    global success
    return result, success


# parse('')
