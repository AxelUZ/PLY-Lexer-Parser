#Variables temporales que son el equivalente a los resultados en los cuadruplos
#Ejemplo t1,t2,t3,t4
class TempVarGenerator:
    def __init__(self):
        self.counter = 0
        self.avail = []

    def next(self):
        if self.avail:
            return self.avail.pop(0)
        else:
            temp_var = f't{self.counter}'
            self.counter += 1
            return temp_var