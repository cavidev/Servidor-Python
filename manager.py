from Conexion import *
from DTO import *

listaObjetos = []
listaTodos = []
listaTodos.extend(listar(Animal))
listaTodos.extend(listar(Enfermedad))
listaTodos.extend(listar(Medicamento))
listaTodos.extend(listarDosis())
listaTodos.extend(listarPrescripciones())
listaTodos.extend(obtenerUsuarioBD())

def Insertar(nombreTabla,nombre,descripcion,foto):
    nuevoObjeto = nombreTabla()
    nuevoObjeto.setNombre(nombre)
    nuevoObjeto.setDescripcion(descripcion)
    nuevoObjeto.setFoto(foto)
    listaObjetos.append(nuevoObjeto)
    listaTodos.append(nuevoObjeto)

def InsertarUsuario(login,password,nombre,permiso,foto):
    nuevoObjeto = Usuario()
    nuevoObjeto.setLogin(login)
    nuevoObjeto.setPassword(password)
    nuevoObjeto.setNombre(nombre)
    nuevoObjeto.setPermiso(permiso)
    nuevoObjeto.setFoto(foto)
    listaObjetos.append(nuevoObjeto)
    listaTodos.append(nuevoObjeto)


def InsertarDosis(id,animal,medicamento,enfermedad,peso,dosis):
    nuevoObjeto = Dosis()
    nuevoObjeto.setID(id)
    #falta un for para evitar que se repita el id
    for i in listaTodos:
        if (i.getClase() == "Animal"):
            if (i.getNombre() == animal):
                nuevoObjeto.setAnimal(animal)
        elif (i.getClase() == "Medicamento"):
            if (i.getNombre() == medicamento):
                nuevoObjeto.setMedicamento(medicamento)
        elif (i.getClase() == "Enfermedad"):
            if (i.getNombre() == enfermedad):
                nuevoObjeto.setEnfermedad(enfermedad)

    if (not nuevoObjeto.getAnimal() or not nuevoObjeto.getMedicamento() or not nuevoObjeto.getEnfermedad()):
        print("No se encontraron los datos solicitados")
    else:
        nuevoObjeto.setPeso(peso)
        nuevoObjeto.setDosis(dosis)
        listaObjetos.append(nuevoObjeto)
        listaTodos.append(nuevoObjeto)

def InsertarPrescripcion(id,usuario,animal,enfermedad,peso,idDosis):
    nuevoObjeto = Prescripcion()
    nuevoObjeto.setID(id)
    # falta un for para evitar que se repita el id
    for i in listaTodos:
        if (i.getClase() == "Animal"):
            if (i.getNombre() == animal):
                nuevoObjeto.setAnimal(animal)
        elif (i.getClase() == "Enfermedad"):
            if (i.getNombre() == enfermedad):
                nuevoObjeto.setEnfermedad(enfermedad)

        elif (i.getClase() == "Dosis"):
            if (i.getID() == idDosis):
                nuevoObjeto.setDosis(idDosis)
        elif (i.getClase() == "Usuario"):
            if (i.getLogin() == usuario):
                nuevoObjeto.setUsuario(usuario)
    if (not nuevoObjeto.getAnimal() or not nuevoObjeto.getDosis() or not nuevoObjeto.getEnfermedad() or not nuevoObjeto.getUsuario()):
        print("No se encontraron los datos solicitados")
    else:
        nuevoObjeto.setPeso(peso)
        nuevoObjeto.setDosis(idDosis)
        listaObjetos.append(nuevoObjeto)
        listaTodos.append(nuevoObjeto)


Insertar(Animal,"Perro","Ladra","Woof")
Insertar(Enfermedad,"Sida","Le dio a Car","Foto de Car")
Insertar(Medicamento,"Cura para el sida","No hay","---")
InsertarUsuario("Blanco707","gb","EstebanB","Admin","6asd6das6das6das6d6s8das8da7sdas5qeadhascbjvas")
InsertarDosis(1,"Perro","Cura para el sida","Sida",10,10)
InsertarPrescripcion(10,"Blanco707","Perro","Sida",10,1)

# for i in listaObjetos:
#     if (i.getClase() == "Animal" or i.getClase() == "Medicamento" or i.getClase() == "Enfermedad"):
#         print(i.nombre + " " + i.descripcion + " " + i.foto)
#     elif i.getClase() == "Usuario":
#         print(i.login,i.password)
#     elif i.getClase() == "Dosis":
#         print(i.id,i.animal,i.medicamento,i.enfermedad)
#     else:
#         print(i.id,i.idDosis)

def obtenerUsuarioManager(login,contrasena):
    listaUsuario = obtenerUsuarioBD()
    for usuario in listaUsuario:
        if(usuario.getLogin() == login and usuario.getPassword() ==contrasena):
            return usuario
    return "error"

def InsertarUsuarioManager1(login,password,nombre,permiso,foto):
    insertarUsuarioBD(login, password, nombre, permiso, foto)
    return "Hola..."