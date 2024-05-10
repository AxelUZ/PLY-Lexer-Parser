from parser import parser
from lexer import lexer
from pprint import pprint

def parse_program(file_path):
    with open(file_path, 'r') as file:
        program_code = file.read()
    result = parser.parse(program_code, lexer=lexer)
    return result

def main():
    print("Por favor, selecciona el archivo que deseas probar:")
    print("1. test1.txt")
    print("2. test2.txt")
    print("3. test3.txt")
    print("4. test4.txt")

    option = input("Ingresa el número de tu opción: ")

    if option == "1":
        file_path = 'test.txt'
    elif option == "2":
        file_path = 'test2.txt'
    elif option == "3":
        file_path = 'test3.txt'
    elif option == "4":
        file_path = 'test4.txt'
    else:
        print("Opción inválida. Por favor, intenta de nuevo.")
        return

    parsed_output = parse_program(file_path)
    print("\nParsed Output:")
    pprint(parsed_output)

if __name__ == "__main__":
    main()

