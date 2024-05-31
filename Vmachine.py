from parser import parser, stack


def parse_program(file_path):
    with open(file_path, 'r') as file:
        program_code = file.read()
    result = parser.parse(program_code)
    return result


def processor_quads(quads):
    #Diccionario para el manejo de la "memoria"
    memory_quads = {}
    #apuntador de cuadriplos para gasos goto
    quad_pointer = 0

    #Se itera la tupla quads y se descompone
    while quad_pointer < len(quads):
        quad = quads[quad_pointer]
        operator, left_operand, right_operand, result = quad

        #para obtener valor de los operandos (solo para ids obtener valor numerico)
        left_value = memory_quads.get(left_operand, left_operand)
        right_value = memory_quads.get(right_operand, right_operand)

        if operator == '+':
            memory_quads[result] = left_value + right_value
            print(left_value, "+", right_value)
            quad_pointer += 1
        elif operator == '-':
            memory_quads[result] = left_value - right_value
            print(left_value, "-", right_value)
            quad_pointer += 1
        elif operator == '*':
            memory_quads[result] = left_value * right_value
            print(left_value, "*", right_value)
            quad_pointer += 1
        elif operator == '/':
            memory_quads[result] = left_value / right_value
            print(left_value, "/", right_value)
            quad_pointer += 1
        elif operator == '=':
            memory_quads[result] = left_value
            print(result, "=", left_value)
            quad_pointer += 1
        elif operator == '>':
            memory_quads[result] = left_value > right_value
            print(left_value, ">", right_value)
            quad_pointer += 1
        elif operator == '<':
            memory_quads[result] = left_value < right_value
            print(left_value, "<", right_value)
            quad_pointer += 1
        elif operator == '!=':
            memory_quads[result] = left_value != right_value
            print(left_value, "!=", right_value)
            quad_pointer += 1
        elif operator == 'print':
            print(memory_quads[result])
            quad_pointer += 1
        elif operator == 'GotoF':
            quad_pointer += 1
            quad_pointer = right_value
            continue  # Saltar la impresion del cuadruplo
        elif operator == 'Goto':
            quad_pointer = right_value
        elif operator == 'GotoV':
            if left_value:  # Si la condición es verdadera
                quad_pointer = right_value
            else:
                quad_pointer += 1
            continue  # Saltar la impresión del cuádruplo en caso de salto
        else:
            raise ValueError(f"Unknown operator {operator}")

        # Imprimir cuádruplo procesado
        print(f"Cuádruplo: ({operator}, {left_operand}, {right_operand}, {result} -> {memory_quads[result]})")
        # Imprimir estado de la memoria
        print(f"Memoria: {memory_quads}\n")

    return memory_quads


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

    parse_program(file_path)

    # Procesar los cuádruplos generados
    print("\nProcesamiento de cuádruplos\n")
    #Procesamos los cuadruplos que parsee
    processor_quads(stack.quads)


if __name__ == "__main__":
    main()
