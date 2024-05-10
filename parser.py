import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('right', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPAREN', 'RPAREN'),
)

def p_program(p):
    'program : PROGRAM ID SEMICOLON optional_vars optional_funcs MAIN body END'
    p[0] = ('program', p[2], p[3], p[4], p[5], p[6])


def p_optional_vars(p):
    '''optional_vars : vars
                     | empty'''
    p[0] = p[1]


def p_vars(p):
    '''vars : vars var_declaration
            | var_declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_var_declaration(p):
    '''var_declaration : VAR ID COLON type SEMICOLON'''
    p[0] = ('var_declaration', p[2], p[4])


def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]


def p_optional_funcs(p):
    '''optional_funcs : funcs
                      | empty'''
    p[0] = p[1]


def p_funcs(p):
    '''funcs : funcs func
             | func'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_func(p):
    '''func : VOID ID LPAREN optional_params RPAREN LBRACE body RBRACE'''
    p[0] = ('func', p[2], p[4], p[7])


def p_optional_params(p):
    '''optional_params : params
                       | empty'''
    p[0] = p[1]


def p_params(p):
    '''params : params COMMA param
              | param'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_param(p):
    '''param : ID COLON type'''
    p[0] = ('param', p[1], p[3])


def p_body(p):
    '''body : LBRACE statements RBRACE'''
    p[0] = p[2]


def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : assign
                 | print_stmt
                 | condition
                 | cycle
                 | func_call'''
    p[0] = p[1]


def p_assign(p):
    '''assign : ID EQUAL expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])


def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    '''term : factor TIMES factor
            | factor DIVIDE factor
            | factor'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | CTE_INT
              | CTE_FLOAT
              | ID'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_print_stmt(p):
    '''print_stmt : PRINT LPAREN CTE_STRING RPAREN SEMICOLON'''
    p[0] = ('print', p[3])


def p_condition(p):
    '''condition : IF LPAREN expression RPAREN body ELSE body'''
    p[0] = ('condition', p[3], p[5], p[7])


def p_cycle(p):
    '''cycle : WHILE LPAREN expression RPAREN body'''
    p[0] = ('cycle', p[3], p[5])


def p_func_call(p):
    '''func_call : ID LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('func_call', p[1], p[3])


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()


