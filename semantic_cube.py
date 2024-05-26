#Diccionario vara la verificacion de operacion entre tipos y verificar resultado
semantic_cube = {
    '+': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('float', 'int'): 'float',
        ('float', 'float'): 'float',
    },
    '-': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('float', 'int'): 'float',
        ('float', 'float'): 'float',
    },
    '*': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('float', 'int'): 'float',
        ('float', 'float'): 'float',
    },
    '/': {
        ('int', 'int'): 'float',
        ('int', 'float'): 'float',
        ('float', 'int'): 'float',
        ('float', 'float'): 'float',
    },
    '>': {
        ('int', 'int'): 'bool',
        ('int', 'float'): 'bool',
        ('float', 'int'): 'bool',
        ('float', 'float'): 'bool',
    },
    '<': {
        ('int', 'int'): 'bool',
        ('int', 'float'): 'bool',
        ('float', 'int'): 'bool',
        ('float', 'float'): 'bool',
    }
}


#Metodo para verificar con operador y operandos
def get_result_type(operator, op1, op2):
    return semantic_cube[operator].get((op1, op2), 'error')
