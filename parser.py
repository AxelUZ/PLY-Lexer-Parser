import ply.yacc as yacc
from lexer import tokens
from function_directory import VariableTable
from quad import Quad
from semantic_cube import get_result_type
from TempVars import TempVarGenerator

var_dir = VariableTable()
stack = Quad()
temp_var = TempVarGenerator()


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
        p[0] = (p[1], p[2], p[3], p[4])


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
    assign : ID seen_assign_ID EQUAL seen_term_EQUAL expression seen_exp_quad_E SEMICOLON
    '''
    #Verificar si el id p[1] esta o no dentro del diccionario de vars osea si esta declarado o no
    var_dir.verify_definition(p[1])
    p[0] = (p[1], p[3], p[5], p[6])


#Regla 6 guardar id de assign
def p_seen_assign_ID(p):
    '''
    seen_assign_ID :
    '''
    stack.PilaO.push(p[-1])


#Regla 7 para guardar igual
def p_seen_term_EQUAL(p):
    '''
    seen_term_EQUAL :
    '''
    stack.POper.push(p[-1])


#Regla 8 para generar quad con igual
def p_seen_exp_quad_E(p):
    '''
    seen_exp_quad_E :
    '''
    if not stack.POper.is_empty() and stack.POper.top() == '=':
        left_Operand = stack.PilaO.pop()
        left_Type = stack.PTypes.pop()
        operator = stack.POper.pop()
        result_Type = left_Type

        if result_Type != 'error':
            right_Operand = stack.PilaO.pop()
            stack.generate_quad(operator, left_Operand, None, right_Operand)
            stack.PilaO.push(right_Operand)
            stack.PTypes.push(result_Type)

        else:
            raise TypeError(f"Type mismatch: {operator} {left_Type}")


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
    '''print : PRINT seen_print_PRINT LPAREN list_print_expression RPAREN SEMICOLON
          | PRINT seen_print_PRINT LPAREN list_print_cte RPAREN SEMICOLON'''
    p[0] = (p[1], p[4])


#Definir una o mas expresion para print
def p_list_print_expression(p):
    '''list_print_expression : expression seen_print_quad_PRINT
              | list_print_expression COMMA seen_print_PARINT_COMMA expression seen_print_quad_PRINT'''
    if len(p) == 3:
        # Lista que contiene expresiones en la primera regla (una expression) (p0 lista resultante a recorrer)
        p[0] = [p[1]]
    else:
        # Una o mas espresiones, concatenar lista ya existente[p1] mas las sig expresiones(p[3])
        p[0] = p[1] + [p[4]]


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


#Regla 11 guardar primer print
def p_seen_print_PRINT(p):
    '''
     seen_print_PRINT :
    '''
    stack.POper.push(p[-1])


#Regla 12 Si vienen commas añadir mas prints por cada comma
def p_seen_print_PARINT_COMMA(p):
    '''
    seen_print_PARINT_COMMA :
    '''
    stack.POper.push("print")


#Regla 13 Generar cuadruplos para print
def p_seen_print_quad_PRINT(p):
    '''
    seen_print_quad_PRINT :
    '''
    if not stack.POper.is_empty() and stack.POper.top() == 'print':
        operand = stack.PilaO.pop()
        operator = stack.POper.pop()
        stack.generate_quad(operator, None, None, operand)


#Defincion para validadores booleanos
def p_expression(p):
    '''
    expression : exp
               | exp GT seen_exp_GT_LT_NE exp seen_exp_quad_G_L_N
               | exp LT seen_exp_GT_LT_NE exp seen_exp_quad_G_L_N
               | exp NE seen_exp_GT_LT_NE exp seen_exp_quad_G_L_N
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[4])


#Regla 9 para guardar mayor que, menor que y diferente de
def p_seen_exp_GT_LT_NE(p):
    '''
    seen_exp_GT_LT_NE :
    '''
    stack.POper.push(p[-1])


#Regla 10 para generar cuadruplos para mayor que, menor que y diferente de
def p_seen_exp_quad_G_L_N(p):
    '''
    seen_exp_quad_G_L_N :
    '''
    if not stack.POper.is_empty() and (
            stack.POper.top() == '>' or stack.POper.top() == '<' or stack.POper.top() == '!='):
        right_Operand = stack.PilaO.pop()
        right_Type = stack.PTypes.pop()
        left_Operand = stack.PilaO.pop()
        left_Type = stack.PTypes.pop()
        operator = stack.POper.pop()
        result_Type = get_result_type(operator, left_Type, right_Type)  #Checar en cubo semantico tipos

        if result_Type != 'error':
            result = temp_var.next()
            stack.generate_quad(operator, left_Operand, right_Operand, result)
            stack.PilaO.push(result)
            stack.PTypes.push(result_Type)

        else:
            raise TypeError(f"Type mismatch: {left_Type} {operator} {right_Type}")


#Definicion para sumas y restas
def p_exp(p):
    '''
    exp : term
        | exp PLUS seen_exp_PLUS_MINUS term seen_exp_quad_P_M
        | exp MINUS seen_exp_PLUS_MINUS term seen_exp_quad_P_M
    '''
    if len(p) == 2:
        p[0] = p[1]
        #Verificacion con signod e suma para regla 2
    elif p[2] == '+':
        p[0] = (p[1], p[2], p[4])
        #Verificacion con signo - para regla 3
    elif p[2] == '-':
        p[0] = (p[1], p[2], p[4])


#Regla 3 para guardar sumas y restas
def p_seen_exp_PLUS_MINUS(p):
    '''
    seen_exp_PLUS_MINUS :
    '''
    stack.POper.push(p[-1])


#Regla 4
def p_seen_exp_quad_P_M(p):
    '''
    seen_exp_quad_P_M :
    '''
    if not stack.POper.is_empty() and (stack.POper.top() == '+' or stack.POper.top() == '-'):
        right_Operand = stack.PilaO.pop()
        right_Type = stack.PTypes.pop()
        left_Operand = stack.PilaO.pop()
        left_Type = stack.PTypes.pop()
        operator = stack.POper.pop()
        result_Type = get_result_type(operator, left_Type, right_Type)

        if result_Type != 'error':
            result = temp_var.next()
            stack.generate_quad(operator, left_Operand, right_Operand, result)
            stack.PilaO.push(result)
            stack.PTypes.push(result_Type)

        else:
            raise TypeError(f"Type mismatch: {left_Type} {operator} {right_Type}")


#Definicion para multiplicaciones y divisiones
def p_term(p):
    '''
    term : factor
         | term TIMES seen_term_TIMES_DIVIDE factor seen_exp_quad_T_D
         | term DIVIDE seen_term_TIMES_DIVIDE factor seen_exp_quad_T_D
    '''
    if len(p) == 2:
        p[0] = p[1]
        # Verificacion con signod e multiplicacion para regla 2
    elif p[2] == '*':
        p[0] = (p[1], p[2], p[4])
        # Verificacion con signod e division para regla 3
    elif p[2] == '/':
        p[0] = (p[1], p[2], p[4])


#Regla 2 para guardar multiplicaciones y divisiones
def p_seen_term_TIMES_DIVIDE(p):
    '''
    seen_term_TIMES_DIVIDE :
    '''
    stack.POper.push(p[-1])


#Regla 5 quads para multiplicacion y division
def p_seen_exp_quad_T_D(p):
    '''
    seen_exp_quad_T_D :
    '''
    if not stack.POper.is_empty() and (stack.POper.top() == '*' or stack.POper.top() == '/'):
        right_Operand = stack.PilaO.pop()
        right_Type = stack.PTypes.pop()
        left_Operand = stack.PilaO.pop()
        left_Type = stack.PTypes.pop()
        operator = stack.POper.pop()
        result_Type = get_result_type(operator, left_Type, right_Type)
        if result_Type != 'error':
            result = temp_var.next()
            stack.generate_quad(operator, left_Operand, right_Operand, result)
            stack.PilaO.push(result)
            stack.PTypes.push(result_Type)

        else:
            raise TypeError(f"Type mismatch: {left_Type} {operator} {right_Type}")


#Op con ultiples parentesis
def p_factor(p):
    '''factor : LPAREN expression RPAREN
           | PLUS ID seen_factor_ID verify_declaration
           | MINUS ID seen_factor_ID verify_declaration
           | PLUS cte
           | MINUS cte
           | ID seen_factor_ID verify_declaration
           | cte'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


#Regla 1 para guardar ids y sus tipos que apunta a factor
def p_seen_factor_ID(p):
    '''
    seen_factor_ID :
    '''
    stack.PilaO.push(p[-1])
    stack.PTypes.push(var_dir.get_variable_type(p[-1]))


def p_verify_declaration(p):
    '''
    verify_declaration :
    '''
    var_dir.verify_definition(p[-2])


def p_cte(p):
    '''cte : CTE_INT seen_INT
        | CTE_FLOAT seen_FLOAT'''
    p[0] = p[1]
    # Regla 14 añadir ctes
    stack.PilaO.push(p[1])


def p_seen_INT(p):
    '''
    seen_INT :
    '''
    stack.PTypes.push('int')


def p_seen_FLOAT(p):
    '''
    seen_FLOAT :
    '''
    stack.PTypes.push('float')


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()
