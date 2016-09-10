class Usuario:
    def __init__(self):
        self.login = ""
        self.password = ""
        self.nombre = ""
        self.permiso = ""
        self.foto = ""
        self.fotoDecodificada = ""

    def getLogin(self):
        return self.login

    def getPassword(self):
        return self.password

    def getNombre(self):
        return self.nombre

    def getPermiso(self):
        return self.permiso

    def getFoto(self):
        return self.foto

    def getFotoDecodificada(self):
        return self.fotoDecodificada

    def setLogin(self, login):
        self.login = login

    def setPassword(self, password):
        self.password = password

    def setNombre(self, nombre):
        self.nombre = nombre

    def setPermiso(self, permiso):
        self.permiso = permiso

    def setFoto(self, foto):
        self.foto = foto

    def setFotoDecodificada(self, fotoDecodificada):
        self.fotoDecodificada = fotoDecodificada

    def getClase(self):
        return "Usuario"


class Medicamento:
    def __init__(self):
        self.nombre = ""
        self.descripcion = ""
        self.foto = ""
        self.fotoDecodificada = ""

    def getNombre(self):
        return self.nombre

    def getDescripcion(self):
        return self.descripcion

    def getFoto(self):
        return self.foto

    def getFotoDecodificada(self):
        return self.fotoDecodificada

    def setNombre(self, nombre):
        self.nombre = nombre

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setFoto(self, foto):
        self.foto = foto

    def setFotoDecodificada(self, fotoDecodificada):
        self.fotoDecodificada = fotoDecodificada

    def getClase(self):
        return "Medicamento"


class Animal:
    def __init__(self):
        self.nombre = ""
        self.descripcion = ""
        self.foto = ""

    def getNombre(self):
        return self.nombre

    def getDescripcion(self):
        return self.descripcion

    def getFoto(self):
        return self.foto

    def setNombre(self, nombre):
        self.nombre = nombre

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setFoto(self, foto):
        self.foto = foto

    def getClase(self):
        return "Animal"


class Enfermedad:
    def __init__(self):
        self.nombre = ""
        self.descripcion = ""
        self.foto = ""

    def getNombre(self):
        return self.nombre

    def getDescripcion(self):
        return self.descripcion

    def getFoto(self):
        return self.foto

    def setNombre(self, nombre):
        self.nombre = nombre

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setFoto(self, foto):
        self.foto = foto

    def getClase(self):
        return "Enfermedad"


class Dosis:
    def __init__(self):
        self.id = 0
        self.animal = ""
        self.medicamento = ""
        self.enfermedad = ""
        self.min = 0
        self.max = 0
        self.dosis = 0

    def getID(self):
        return self.id

    def getAnimal(self):
        return self.animal

    def getMedicamento(self):
        return self.medicamento

    def getEnfermedad(self):
        return self.enfermedad

    def getMinPeso(self):
        return self.min

    def getMaxPeso(self):
        return self.max

    def getDosis(self):
        return self.dosis

    def setID(self, ident):
        self.id = ident

    def setAnimal(self, animal):
        self.animal = animal

    def setMedicamento(self, medicamento):
        self.medicamento = medicamento

    def setEnfermedad(self, enfermedad):
        self.enfermedad = enfermedad

    def setRangoPeso(self, min, max):
        self.min = min
        self.max = max

    def setDosis(self, dosis):
        self.dosis = dosis

    def getClase(self):
        return "Dosis"


class Prescripcion:
    def __init__(self):
        self.id = 0
        self.usuario = ""
        self.animal = ""
        self.enfermedad = ""
        self.peso = 0
        self.idDosis = 0

    def getID(self):
        return self.id

    def getUsuario(self):
        return self.usuario

    def getAnimal(self):
        return self.animal

    def getEnfermedad(self):
        return self.enfermedad

    def getPeso(self):
        return self.peso

    def getDosis(self):
        return self.idDosis

    def setID(self, ident):
        self.id = ident

    def setUsuario(self, usuario):
        self.usuario = usuario

    def setAnimal(self, animal):
        self.animal = animal

    def setEnfermedad(self, enfermedad):
        self.enfermedad = enfermedad

    def setPeso(self, peso):
        self.peso = peso

    def setDosis(self, dosis):
        self.idDosis = dosis

    def getClase(self):
        return "Prescripcion"
