import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('right', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'LBRACE', 'RBRACE'),
    ('left', 'LBRACKET', 'RBRACKET'),
)


def p_program(p):
    '''program : PROGRAM ID SEMICOLON vars funcs MAIN body END'''
    p[0] = ('program', p[2], p[4], p[5], p[7])


def p_vars(p):
    '''
    vars : VAR ID COLON type SEMICOLON
         | VAR ID COLON type SEMICOLON vars
    '''
    if len(p) == 6:
        p[0] = [('var_declaration', p[2], p[4])]
    else:
        p[0] = [('var_declaration', p[2], p[4])] + p[6]


def p_type(p):
    '''
    type : INT
         | FLOAT
    '''
    p[0] = p[1]


def p_body(p):
    '''
    body : LBRACE statement RBRACE
    '''
    p[0] = p[2]


#2 func
def p_function_params(p):
    '''
    function_params : ID COLON type
                    | function_params COMMA ID COLON type
    '''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = p[1] + [(p[3], p[5])]


#1 func
def p_funcs(p):
    '''
    funcs : VOID ID LPAREN function_params RPAREN LBRACKET vars body RBRACKET SEMICOLON
          | VOID ID LPAREN function_params RPAREN LBRACKET vars body RBRACKET SEMICOLON funcs
          | VOID ID LPAREN RPAREN LBRACKET vars body RBRACKET SEMICOLON
          | VOID ID LPAREN RPAREN LBRACKET vars body RBRACKET SEMICOLON funcs
    '''
    if len(p) == 8:
        p[0] = ('function', p[2], p[4], p[6], p[7])
    else:
        p[0] = [('function', p[2], p[4], p[6], p[7])]


def p_statement(p):
    '''
    statement : assign
              | condition
              | cycle
              | f_call
              | print
    '''
    p[0] = p[1]


def p_assign(p):
    '''assign : ID EQUAL expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])


def p_condition(p):
    '''
    condition : IF LPAREN expression RPAREN body
              | IF LPAREN expression RPAREN body ELSE body
    '''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if-else', p[3], p[5], p[7])


def p_cycle(p):
    '''
    cycle : DO body WHILE LPAREN expression RPAREN SEMICOLON
    '''
    p[0] = ('do_while', p[2], p[5])


#f_call 1
def p_f_call(p):
    '''
    f_call : ID LPAREN optional_arguments RPAREN SEMICOLON
    '''
    p[0] = ('func_call', p[1], p[3])


#f_call 2
def p_optional_arguments(p):
    '''
    optional_arguments : expression
                        | optional_arguments COMMA expression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_print(p):
    '''
    print : PRINT LPAREN expression RPAREN SEMICOLON
                    | PRINT LPAREN CTE_STRING RPAREN SEMICOLON
    '''
    if len(p) == 6:
        p[0] = ('print', p[3])


def p_expression(p):
    '''
    expression : exp
               | exp GT exp
               | exp LT exp
               | exp NE exp
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_exp(p):
    '''
    exp : term
        | exp PLUS term
        | exp MINUS term
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = ('add', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('subtract', p[1], p[3])


def p_term(p):
    '''
    term : factor
         | term TIMES factor
         | term DIVIDE factor
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = ('multiply', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('divide', p[1], p[3])


def p_factor(p):
    '''
    factor : LPAREN expression RPAREN
           | PLUS ID
           | MINUS ID
           | PLUS cte
           | MINUS cte
           | ID
           | cte
    '''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = ('unary_op', p[1], p[2])
    else:
        p[0] = p[1]


def p_cte(p):
    '''
    cte : CTE_INT
        | CTE_FLOAT
    '''
    if isinstance(p[1], int):
        p[0] = ('cte_int', p[1])
    elif isinstance(p[1], float):
        p[0] = ('cte_float', p[1])


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()
