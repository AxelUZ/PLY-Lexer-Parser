class VariableTable:
    def __init__(self):
        self.variables = {}

    # Añadir variable y tipo y verificar si ya fue declarada
    def add_variable(self, name, var_type):
        if name in self.variables:
            raise ValueError(f"Variable '{name}' already declared.")
        self.variables[name] = var_type

    # Verificar variables que se encuentren para saber si se declararon
    def verify_definition(self, name):
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not declared.")
        return name in self.variables

    def get_variable(self, name):
        return self.variables.get(name, None)

    # Obtener el tipo de una variable dado su nombre
    def get_variable_type(self, name):
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not declared.")
        return self.variables[name]

    def __repr__(self):
        return str(self.variables)
