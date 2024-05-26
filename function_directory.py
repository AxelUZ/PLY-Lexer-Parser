class VariableTable:
    def __init__(self):
        self.variables = {}

    def add_variable(self, name, var_type):
        if name in self.variables:
            raise ValueError(f"Variable '{name}' already declared.")
        self.variables[name] = var_type

    def verify_definition(self, name):
        if name not in self.variables:
            raise ValueError(f"Variable '{name}' not declared.")
        return name in self.variables

    def get_variable(self, name):
        return self.variables.get(name, None)

    def __repr__(self):
        return str(self.variables)