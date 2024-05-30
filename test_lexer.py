import lexer


def test_lexer(input_string):
    lexer.lexer.input(input_string)
    for tok in lexer.lexer:
        print(tok)


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

    with open(file_path, 'r') as file:
        file_content = file.read()

    test_lexer(file_content)


if __name__ == "__main__":
    main()
