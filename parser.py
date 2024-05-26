import ply.yacc as yacc
from lexer import tokens
from function_directory import VariableTable

var_dir = VariableTable()

precedence = (
    ('right', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'LBRACE', 'RBRACE'),
)


def p_program(p):
    '''program : PROGRAM ID SEMICOLON return_vars MAIN body END
               | PROGRAM ID SEMICOLON MAIN body END'''
    if len(p) == 8:
        # Hay variables
        p[0] = ("Vars", p[1], p[2], p[4], p[5], p[6], p[7])
    else:
        # No hay variables
        p[0] = ("No Vars", p[1], p[2], p[4], p[5], p[6])


#Regla para rtornarte y definir vars de mas tipos
def p_return_vars(p):
    '''return_vars : vars
                | return_vars vars'''
    if len(p) == 2:
        #Caso en el que no se retorna
        p[0] = [p[1]]
    else:
        #Caso para retorno y definicion de otro tipo de var concatenar lista ya existente mas la que venga del retorno
        p[0] = [p[1]] + [p[2]]


#Definicion clasica de lo que constituye una declaración
def p_vars(p):
    '''vars : VAR list_vars COLON type SEMICOLON
         | list_vars COLON type SEMICOLON'''
    if len(p) == 6:
        p[0] = (p[1], p[2], p[3], p[4], p[5])
        #Recorrer la lista list_vars y añadir ids y tipos (Concatenar para regla 1)
        for vars_p2 in p[2]:
            var_dir.add_variable(vars_p2, p[4])
    else:
        #Concatenar para regla 2 en caso de que se haga el return entre VAR y ID
        for vars_p1 in p[1]:
            var_dir.add_variable(vars_p1, p[3])


#Definir una o mas variables
def p_list_vars(p):
    '''list_vars : ID
              | list_vars COMMA ID'''
    if len(p) == 2:
        # Lista que contiene ID en la primera regla (una Var) (p0 lista resultante a recorrer)
        p[0] = [p[1]]
    else:
        # Una o mas vars, concatenar lista ya existente[p1] mas los ID(p[3])
        p[0] = p[1] + [p[3]]


#Tipos en la def de variables
def p_type(p):
    '''type : INT
         | FLOAT'''
    p[0] = p[1]


#Repetir el statement dentro del body teniendo uno o mas statement
def p_return_statement(p):
    '''return_statement : statement
                     | return_statement statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        #Concatenar los statements que ya se tenian con los nuevos
        p[0] = p[1] + [p[2]]


#Defincion clasica del body
def p_body(p):
    '''
    body : LBRACE return_statement RBRACE
    '''
    #Lista de statements
    p[0] = [(p[1], p[2], p[3])]


#Definicion de los statement donde se usa empty para el salto del statement
def p_statement(p):
    '''statement : assign
              | condition
              | cycle
              | print
              | empty'''
    p[0] = p[1]


#Definicion general del assign
def p_assign(p):
    '''
    assign : ID EQUAL expression SEMICOLON
    '''
    #Verificar si el id p[1] esta o no dentro del diccionario de vars osea si esta declarado o no
    var_dir.verify_definition(p[1])
    p[0] = (p[1], p[2])


#Definicion general de if con y sin else
def p_condition(p):
    '''condition : IF LPAREN expression RPAREN body
              | IF LPAREN expression RPAREN body ELSE body'''
    if len(p) == 6:
        #Caso para If
        p[0] = (p[1], p[3], p[5])
    else:
        #Caso para If Else
        p[0] = (p[1], p[3], p[5], p[6], p[7])


#Definicion para do while
def p_cycle(p):
    '''
    cycle : DO body WHILE LPAREN expression RPAREN SEMICOLON
    '''
    p[0] = (p[1], p[2], p[3], p[5])


#Definicion de print
def p_print(p):
    '''print : PRINT LPAREN list_print_expression RPAREN SEMICOLON
          | PRINT LPAREN list_print_cte RPAREN SEMICOLON'''
    p[0] = (p[1], p[3])


#Definir una o mas expresion para print
def p_list_print_expression(p):
    '''list_print_expression : expression
              | list_print_expression COMMA expression'''
    if len(p) == 2:
        # Lista que contiene expresiones en la primera regla (una expression) (p0 lista resultante a recorrer)
        p[0] = [p[1]]
    else:
        # Una o mas espresiones, concatenar lista ya existente[p1] mas las sig expresiones(p[3])
        p[0] = p[1] + [p[3]]


#Definir una o mas strings en un print
def p_list_print_cte(p):
    '''list_print_cte : CTE_STRING
              | list_print_cte COMMA CTE_STRING'''
    if len(p) == 2:
        # Lista que contiene string en la primera regla (una string) (p0 lista resultante a recorrer)
        p[0] = [p[1]]
    else:
        # Una o mas strings, concatenar lista ya existente[p1] mas los sig strings (p[3])
        p[0] = p[1] + [p[3]]


#Defincion para validadores booleanos
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
        p[0] = (p[1], p[2], p[3])


#Definicion para sumas y restas
def p_exp(p):
    '''
    exp : term
        | exp PLUS term
        | exp MINUS term
    '''
    if len(p) == 2:
        p[0] = p[1]
        #Verificacion con signod e suma para regla 2
    elif p[2] == '+':
        p[0] = (p[1], p[2], p[3])
        #Verificacion con signo - para regla 3
    elif p[2] == '-':
        p[0] = (p[1], p[2], p[3])


#Definicion para multiplicaciones y divisiones
def p_term(p):
    '''
    term : factor
         | term TIMES factor
         | term DIVIDE factor
    '''
    if len(p) == 2:
        p[0] = p[1]
        # Verificacion con signod e multiplicacion para regla 2
    elif p[2] == '*':
        p[0] = (p[1], p[2], p[3])
        # Verificacion con signod e division para regla 3
    elif p[2] == '/':
        p[0] = (p[1], p[2], p[3])

#Op con ultiples parentesis
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
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 3:
        var_dir.verify_definition(p[2])
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_cte(p):
    '''
    cte : CTE_INT
        | CTE_FLOAT
    '''
    p[0] = p[1]


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()
