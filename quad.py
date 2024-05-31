class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    def top(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("top from empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def __repr__(self):
        return repr(self.items)


class Quad:
    def __init__(self):
        self.POper = Stack()  # Pila de operadores +,-,=
        self.PilaO = Stack()  # Pila de operandos x,y,z
        self.PTypes = Stack()  # Pila de tipos de operandos
        self.PJumps = Stack()  # Pila de saltos
        self.quads = []  # Tupla de cuádruplos

    def generate_quad(self, operator, left_operand, right_operand, result):
        quad = (operator, left_operand, right_operand, result)
        self.quads.append(quad)
        return quad

    def fill(self, quad_index, fill_value):
        operator, left_operand, _, result = self.quads[quad_index]
        self.quads[quad_index] = (operator, left_operand, fill_value, result)