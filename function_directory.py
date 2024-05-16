class VariableTable:
    def __init__(self):
        self.variables = {}

    def add_variable(self, name, var_type):
        if name in self.variables:
            raise ValueError(f"Variable '{name}' already declared.")
        self.variables[name] = var_type

    def get_variable(self, name):
        return self.variables.get(name, None)

    def __repr__(self):
        return str(self.variables)


class FunctionDirectory:
    def __init__(self):
        self.functions = {}

    def add_function(self, name, return_type):
        if name in self.functions:
            raise ValueError(f"Function '{name}' already declared.")
        self.functions[name] = {
            'return_type': return_type,
            'var_table': VariableTable()
        }

    def add_variable_to_function(self, func_name, var_name, var_type):
        if func_name not in self.functions:
            raise ValueError(f"Function '{func_name}' not declared.")
        self.functions[func_name]['var_table'].add_variable(var_name, var_type)

    def get_function(self, name):
        return self.functions.get(name, None)

    def __repr__(self):
        return str(self.functions)
