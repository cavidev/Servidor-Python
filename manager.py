import base64

from Conexion import *
from DTO import *
from flask import request

#Listas Temporales
listaAEM = []
listaUsuarios = []
listaDosis = []
listaPrescripciones = []
# Listas Generales
generalAEM = []
generalAEM.extend(listar(Animal))
generalAEM.extend(listar(Medicamento))
generalAEM.extend(listar(Enfermedad))
generalUsuarios = obtenerUsuarioBD()
generalDosis = listarDosis()
generalPrescripciones = listarPrescripciones()

def InsertarManager(nombreTabla,request):
    nuevoObjeto = nombreTabla()
    nuevoObjeto.setNombre(request.form['nombre'])
    nuevoObjeto.setDescripcion(request.form['descripcion'])

    listaAEM.append(nuevoObjeto)
    generalAEM.append(nuevoObjeto)
    print("Mae instacie el objeto y lo agrege: ")

def Insertar(nombreTabla,nombre,descripcion,foto):
    nuevoObjeto = nombreTabla()
    nuevoObjeto.setNombre(nombre)
    nuevoObjeto.setDescripcion(descripcion)
    nuevoObjeto.setFoto(foto)
    listaAEM.append(nuevoObjeto)
    generalAEM.append(nuevoObjeto)

def InsertarUsuario(request):
    tempLista = list(filter(lambda x: x.getLogin() == request.form["usuario"],generalUsuarios))
    if len(tempLista) > 0 :
        print("Ya existe un usuario con ese ID")
    else:
        nuevoObjeto = Usuario()
        nuevoObjeto.setLogin(request.form["usuario"])
        nuevoObjeto.setPassword(request.form['contrasena'])
        nuevoObjeto.setNombre(request.form['nombreCompleto'])
        nuevoObjeto.setPermiso(request.form['permiso'])
        foto = request.files['fotoSubida']
        valor = base64.b64encode(foto.getvalue())
        resultado = valor.decode('utf8')
        nuevoObjeto.setFoto(resultado)
        listaUsuarios.append(nuevoObjeto)
        generalUsuarios.append(nuevoObjeto)

def InsertarDosis(id,animal,medicamento,enfermedad,peso,dosis):
    tempLista = list(filter(lambda x: x.getID() == id, generalDosis))
    if (len(tempLista)>0):
        print("Ya existe una dosis con ese ID")
    else:
        nuevoObjeto = Dosis()
        nuevoObjeto.setID(id)
        tempLista = list(filter(lambda x: (x.getClase() == "Animal" and x.getNombre() == animal) or
                                          (x.getClase() == "Medicamento" and x.getNombre() == medicamento) or
                                          (x.getClase() == "Enfermedad" and x.getNombre() == enfermedad)
                                           ,generalAEM))
        if (len(tempLista) != 3):
            print("No se encontraron los datos solicitados")
        else:
            nuevoObjeto.setPeso(peso)
            nuevoObjeto.setDosis(dosis)
            listaDosis.append(nuevoObjeto)
            generalDosis.append(nuevoObjeto)

def InsertarPrescripcion(id,usuario,animal,enfermedad,peso,idDosis):
    tempLista = list(filter(lambda x: x.getID() == id, generalPrescripciones))
    if (len(tempLista> 0)):
        print("Ya existe una prescripcion con esa ID")
    else:
        nuevoObjeto = Prescripcion()
        nuevoObjeto.setID(id)
        # falta un for para evitar que se repita el id
        tempAEM = list(filter(lambda x: (x.getClase() == "Animal" and x.getNombre() == animal) or
                                          (x.getClase() == "Enfermedad" and x.getNombre() == enfermedad)
                                , generalAEM))
        tempUsuario = list(filter(lambda y: y.getLogin() == usuario,generalUsuarios))
        tempDosis = list(filter(lambda z: z.getID() == idDosis,generalDosis))
        if (len(tempAEM) != 2 or len(tempUsuario) != 1 or len(tempDosis) != 1):
            print("No se encontraron los datos solicitados")
        else:

            nuevoObjeto.setPeso(peso)
            nuevoObjeto.setDosis(idDosis)
            listaPrescripciones.append(nuevoObjeto)
            generalPrescripciones.append(nuevoObjeto)


# Insertar(Animal,"Perro","Ladra","Woof")
# Insertar(Animal,"Gato","Maulla","Miau")
# Insertar(Enfermedad,"Sida","Le dio a Car","Foto de Car")
# Insertar(Enfermedad,"Gonorrea","WTF","Foto de gonorrea")
# Insertar(Medicamento,"Cura para el sida","No hay","---")
# Insertar(Medicamento,"Crema de rosas","Para la piel reseca","---")
# InsertarUsuario("Blanco707","gb","EstebanB","Admin","6asd6das6das6das6d6s8das8da7sdas5qeadhascbjvas")
# InsertarDosis(1,"Perro","Cura para el sida","Sida",10,10)
# InsertarPrescripcion(10,"Blanco707","Perro","Sida",10,1)

def obtenerUsuarioManager(login,contrasena):
    listaUsuario = obtenerUsuarioBD()
    for usuario in listaUsuario:
        if usuario.getLogin() == login and usuario.getPassword() == contrasena:
            return usuario
    return "error"

def InsertarUsuarioManager1(login,password,nombre,permiso,foto):
    return insertarUsuarioBD(login, password, nombre, permiso, foto)

def Modificar(stringTabla, request):
    tempLista = list(filter(lambda x: x.getNombre() == request.form["nombre"]))


