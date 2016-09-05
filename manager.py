

class Persona:
    nombre = ""
    apellido = ""
    def __init__ (self,nombre,apellido):
        self.nombre = nombre
        self.apellido = apellido
    def getNombre(self):
        return self.nombre + " " + self.apellido

persona1 = Persona("Carlos","Villafuerte")

def salude():
    comida = ["Carlos", "Esteban", "Irina", "Alejandra"]
    return comida