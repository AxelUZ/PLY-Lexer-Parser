import ply.lex as lex

#Lista de tokens
tokens = [
    'PROGRAM',
    'VAR',
    'INT',
    'FLOAT',
    'PRINT',
    'IF',
    'ELSE',
    'WHILE',
    'DO',
    'VOID',
    'MAIN',
    'END',
    'SEMICOLON',
    'COMMA',
    'COLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'EQUAL',
    'GT',
    'LT',
    'NE',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ID',
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_STRING'
]

#Definicion de tokens
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUAL = r'='
t_GT = r'>'
t_LT = r'<'
t_NE = r'!='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

#Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'void': 'VOID',
    'main': 'MAIN',
    'end': 'END'
}

#Definicion tokens complejos
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CTE_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()