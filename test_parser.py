from parser import parser
from lexer import lexer


def parse_program(file_path):
    with open(file_path, 'r') as file:
        program_code = file.read()
    result = parser.parse(program_code, lexer=lexer)
    return result


file_path = 'test.txt'
parsed_output = parse_program(file_path)
print("Parsed Output:", parsed_output)
