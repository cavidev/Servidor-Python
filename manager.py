import base64
from Conexion import *
from DTO import *
from flask import request

# Listas Temporales
listaAEM = []
listaUsuarios = []
listaDosis = []
listaPrescripciones = []

def LimpiarListasLocales():
    listaAEM.clear()
    listaUsuarios.clear()
    listaDosis.clear()
    listaPrescripciones.clear()

# Listas Generales
generalAEM = []
generalUsuarios = []
generalDosis = []
generalPrescripciones = []

def CargarListasGenerales():
    global generalAEM,generalUsuarios,generalDosis,generalPrescripciones
    generalAEM.extend(listar(Animal))
    generalAEM.extend(listar(Medicamento))
    generalAEM.extend(listar(Enfermedad))
    generalUsuarios = obtenerUsuarioBD()
    generalDosis = listarDosis()
    generalPrescripciones = listarPrescripciones()

CargarListasGenerales()

# Contador Global
contador  = 0
def AumentarContador():
    global contador
    contador = contador+1

# Generadores
def generadorAEM():
    global contador
    while True:
        yield listaAEM[contador]

def generadorUsuarios():
    global contador
    while True:
        yield listaUsuarios[contador]

def generadorDosis():
    global contador
    while True:
        yield listaDosis[contador]

def generadorPrescripciones():
    global contador
    while True:
        yield listaPrescripciones[contador]

gAEM = generadorAEM()
gUsuarios = generadorUsuarios()
gDosis = generadorDosis()
gPresc = generadorPrescripciones()

# Ya se reviso!!
def InsertarUsuario(request):
    """Verifica que un usuario no tuviera el mismo ID, if agrega un usuario nuevo
    a la lista respectiva de los usuario
    Parametros:
        request = datos insertados en un formularios en html,
        el archivo imagen que recibe se codefica en ut8 para ser almacenado.
    Returns:
        Estado de la inserción"""
    tempLista = list(filter(lambda x: x.getLogin() == request.form["usuario"], generalUsuarios))
    if len(tempLista) > 0:
        return "¡¡ Ya existe un usuario con ese ID !!"
    else:
        nuevoObjeto = Usuario()
        nuevoObjeto.setLogin(request.form["usuario"])
        nuevoObjeto.setPassword(request.form['contrasena'])
        nuevoObjeto.setNombre(request.form['nombreCompleto'])
        nuevoObjeto.setPermiso(request.form['permiso'])
        foto = request.files['foto']
        valor = base64.b64encode(foto.getvalue())
        resultado = valor.decode('utf8')
        print(resultado)
        nuevoObjeto.setFoto(resultado)
        listaUsuarios.append(nuevoObjeto)
        generalUsuarios.append(nuevoObjeto)
        return "¡¡ Se agrego a la lista de espera !!"


# Ya se reviso!!
def InsertarManager(nombreTabla, request):
    """Agrega medicamentos/animales/enfermedades al sistema,
    de forma generica hara el objeto.
    :parameter
        nombreTabla: Constructor del objeto correspondiente.
        request: datos insertados en html, se decodifica la imagen en utf8
            para poder ser guardada.
    :returns
        Estado de la inserción"""
    nuevoObjeto = nombreTabla()
    nuevoObjeto.setNombre(request.form['nombre'])
    nuevoObjeto.setDescripcion(request.form['descripcion'])
    # Con esto se agrega la foto decodificada
    foto = request.files['foto']
    valor = base64.b64encode(foto.getvalue())
    resultado = valor.decode('utf8')
    print(resultado)
    nuevoObjeto.setFoto(resultado)
    # ---------------------------------------
    listaAEM.append(nuevoObjeto)
    generalAEM.append(nuevoObjeto)
    return "¡¡ Se agrego a la lista: " + nuevoObjeto.getClase() + "=> " + nuevoObjeto.getNombre() + "!!"


def InsertarDosis(request):
    """Crea un objeto con la dosis recomendada por el usuario en la lista respectiva,
    verifica por medio de lambda que no exista una dosis con el mismo ID
    y que animal,medicamento y enfermedad existen en sistema.
    :parameter
        reques: Datos insertados en el html.
    :return
        Estado de la inserción.
    """
    id = request.form['idDosis']
    tempLista = list(filter(lambda x: x.getID() == id, generalDosis))
    if len(tempLista) > 0:
        return "¡¡ Ya existe una dosis con ese ID !!"
    else:
        animal = request.form['animal']
        medicamento = request.form['medicamento']
        enfermedad = request.form['enfermedad']
        #verifica lambda
        for item in generalAEM:
            print(item.getNombre())
        tempLista = list(filter(lambda x: (x.getClase() == "Animal" and x.getNombre() == animal) or
                                          (x.getClase() == "Medicamento" and x.getNombre() == medicamento) or
                                          (x.getClase() == "Enfermedad" and x.getNombre() == enfermedad)
                                , generalAEM))
        if (len(tempLista) != 3):
            return "¡¡ Verifique el animal, medicamento o enfermedad !!"
        else:
            nuevoObjeto = Dosis()
            nuevoObjeto.setID(id)
            nuevoObjeto.setAnimal(animal)
            nuevoObjeto.setMedicamento(medicamento)
            nuevoObjeto.setEnfermedad(enfermedad)
            nuevoObjeto.setRangoPeso(request.form['min'], request.form['max'])
            nuevoObjeto.setDosis(request.form['dosis'])
            listaDosis.append(nuevoObjeto)
            generalDosis.append(nuevoObjeto)
            return "¡¡ Se insertaron los datos con exito !!"


def InsertarPrescripcion(request):
    """Crea y agrega un objeto a la lista correspondiente, por medio de lambda verifica
    que no tengan los mismo ID y que la informacion de llave primaria si aparezca en la BD

    :parameter
        request: Datos insertados por medio del html
    :return
        El estdo de la insercion.
    """
    id = request.form['idPrescripcion']
    usuario = request.form['usuario']
    animal = request.form['animal']
    enfermedad = request.form['enfermedad']
    idDosis = request.form['idDosis']

    if len(list(filter(lambda x: x.getID() == id, generalPrescripciones))) > 0:
        return "¡¡ Ya existe una prescripcion con esa ID !!"
    else:
        tempAEM = list(filter(lambda x: (x.getClase() == "Animal" and x.getNombre() == animal) or
                                        (x.getClase() == "Enfermedad" and x.getNombre() == enfermedad)
                              , generalAEM))
        tempUsuario = list(filter(lambda y: y.getLogin() == usuario, generalUsuarios))
        tempDosis = list(filter(lambda z: z.getID() == idDosis, generalDosis))

        if len(tempAEM) != 2 or len(tempUsuario) != 1 or len(tempDosis) != 1:
            return "¡¡ No se encontraron los datos solicitados !!"
        else:
            nuevoObjeto = Prescripcion()
            nuevoObjeto.setID(id)
            nuevoObjeto.setUsuario(usuario)
            nuevoObjeto.setAnimal(animal)
            nuevoObjeto.setEnfermedad(enfermedad)
            nuevoObjeto.setPeso(request.form['peso'])
            nuevoObjeto.setDosis(idDosis)
            listaPrescripciones.append(nuevoObjeto)
            generalPrescripciones.append(nuevoObjeto)
            return "¡¡ Se inserto con exito !!"


def obtenerUsuarioManager(login, contrasena):
    """Obtien el usuario que se esta logeando,
    Parametros:
        login: Nombre de usuario
        contrasena: La contraseña del usuario.
    Returns:
        Usuario if encuentra else estado de la busqueda."""
    listaUsuario = obtenerUsuarioBD()
    listaGenerada = list(filter(lambda x: x.getLogin() == login and x.getPassword() == contrasena, listaUsuario))
    if 0 < len(listaGenerada):
        return listaGenerada[0]
    else:
        return "error"


def ObtenerAnimales():
    """Retorna una lista con los animales de toda la BD,
    usa una función lambda"""
    lista = list(filter(lambda x: x.getClase() == "Animal", listaAEM))
    if 0 < len(lista):
        return lista
    else:
        return "error"


def ObternerMedicamentos():
    """Retorna una lista con los medicamentos de toda la BD,
    usa una función lambda"""
    lista = list(filter(lambda x: x.getClase() == "Medicamento", listaAEM))
    if 0 < len(lista):
        return "error"
    else:
        return lista


def ObtenerEnfermedad():
    """Retorna una lista con los animales de toda la BD,
    usa una función lambda"""
    lista = list(filter(lambda x: x.getClase() == "Enfermedad", listaAEM))
    if 0 < len(lista):
        return "error"
    else:
        return lista


def InsertarUsuarioManager1(login, password, nombre, permiso, foto):
    'Inserta el usuario directamente en la BD.'
    return insertarUsuarioBD(login, password, nombre, permiso, foto)


def Modificar(stringTabla, request):
    nombre = request.form["nombre"]
    nuevaDesc = request.form["descripcion"]
    foto = request.files['foto']
    valor = base64.b64encode(foto.getvalue())
    nuevaFoto = valor.decode('utf8')
    if len(list(filter(lambda x: x.getClase() == stringTabla and x.getNombre() == nombre, listaAEM))) > 0:
        list(map(lambda x: [x.setDescripcion(nuevaDesc),
                            x.setFoto(nuevaFoto)] if x.getClase() == stringTabla and x.getNombre() == nombre else ' ', listaAEM))
        list(map(lambda x: [x.setDescripcion(nuevaDesc),
                            x.setFoto(nuevaFoto)] if x.getClase() == stringTabla and x.getNombre() == nombre else ' ',
                 generalAEM))
    else:
        resultadoQ = ModificarBD(stringTabla,nuevaDesc,nuevaFoto,nombre)
        if resultadoQ == 0:
            print("No se encontró el elemento solicitado")
        else:
            list(map(lambda x: [x.setDescripcion(nuevaDesc),
                                x.setFoto(nuevaFoto)] if x.getClase() == stringTabla and x.getNombre() == nombre else ' ',
                                generalAEM))

def ModificarUsuario(request):
    usuario = request.form["usuario"]
    contra = request.form['contrasena']
    nombreCompleto = request.form['nombreCompleto']
    permiso = request.form['permiso']
    foto = request.files['foto']
    valor = base64.b64encode(foto.getvalue())
    resultado = valor.decode('utf8')
    if len(list(filter(lambda x: x.getLogin() == usuario, listaUsuarios))) > 0:
        list(map(lambda x: [x.setPassword(contra),x.setNombre(nombreCompleto),x.setPermiso(permiso),x.setFoto(resultado)]
            if x.getLogin() == usuario else ' ', listaUsuarios))
        list(map(lambda x: [x.setPassword(contra), x.setNombre(nombreCompleto), x.setPermiso(permiso), x.setFoto(resultado)]
            if x.getLogin() == usuario else ' ', generalUsuarios))
    else:
        resultadoQ = ModificarUsuarioBD(contra,nombreCompleto,permiso,resultado,usuario)
        if resultadoQ == 0:
            print("No se encontró el elemento solicitado")
        else:
            list(map(lambda x: [x.setPassword(contra), x.setNombre(nombreCompleto), x.setPermiso(permiso),
                                x.setFoto(resultado)] if x.getLogin() == usuario else ' ', generalUsuarios))


def ModificarDosis(request):
    id = request.form['idDosis']
    animal = request.form['animal']
    medicamento = request.form['medicamento']
    enfermedad = request.form['enfermedad']
    minPeso = request.form['min']
    maxPeso = request.form['max']
    dosis = request.form['dosis']
    if (len(list(filter(lambda x:   (x.getClase() == "Animal" and x.getNombre() == animal) or
                                    (x.getClase() == "Medicamento" and x.getNombre() == medicamento) or
                                    (x.getClase() == "Enfermedad" and x.getNombre() == enfermedad)
                                    , generalAEM))) != 3):
        return "¡¡ Verifique el animal, medicamento o enfermedad !!"
    else:
        if len(list(filter(lambda x: x.getID() == id, listaDosis))) > 0:
            list(map(lambda x: [x.setAnimal(animal), x.setMedicamento(medicamento), x.setEnfemedad(enfermedad),
                                x.setRangoPeso(minPeso,maxPeso), x.setDosis(dosis)]
                                if x.getID() == id else ' ', listaDosis))
            list(map(lambda x: [x.setAnimal(animal), x.setMedicamento(medicamento), x.setEnfemedad(enfermedad),
                                x.setRangoPeso(minPeso, maxPeso), x.setDosis(dosis)]
                                if x.getID() == id else ' ', generalDosis))
        else:
            resultadoQ = ModificarDosisBD(animal,medicamento,enfermedad,minPeso,maxPeso,dosis,id)
            if resultadoQ == 0:
                print("No se encontró el elemento solicitado")
            else:
                list(map(lambda x: [x.setAnimal(animal), x.setMedicamento(medicamento), x.setEnfemedad(enfermedad),
                                    x.setRangoPeso(minPeso, maxPeso), x.setDosis(dosis)]
                                    if x.getID() == id else ' ', generalDosis))

def ModificarPrescripcion(request):
    id = request.form['idPrescripcion']
    usuario = request.form['usuario']
    animal = request.form['animal']
    enfermedad = request.form['enfermedad']
    peso = request.form['peso']
    idDosis = request.form['idDosis']
    tempAEM = list(filter(lambda x: (x.getClase() == "Animal" and x.getNombre() == animal) or
                                    (x.getClase() == "Enfermedad" and x.getNombre() == enfermedad)
                                    , generalAEM))
    tempUsuario = list(filter(lambda y: y.getLogin() == usuario, generalUsuarios))
    tempDosis = list(filter(lambda z: z.getID() == idDosis, generalDosis))

    if len(tempAEM) != 2 or len(tempUsuario) != 1 or len(tempDosis) != 1:
        return "¡¡ No se encontraron los datos solicitados !!"
    else:
        if len(list(filter(lambda x: x.getID() == id, generalPrescripciones))) > 0:
            list(map(lambda x: [x.setUsuario(usuario),x.setAnimal(animal),x.setEnfemedad(enfermedad),
                                x.setPeso(peso),x.setDosis(idDosis)]
                                if x.getID() == id else ' ', listaPrescripciones))
            list(map(lambda x: [x.setUsuario(usuario), x.setAnimal(animal), x.setEnfemedad(enfermedad),
                                x.setPeso(peso), x.setDosis(idDosis)]
                                if x.getID() == id else ' ', generalPrescripciones))
        else:
            resultadoQ = ModificarPrescripcionBD(usuario, animal, enfermedad,peso, idDosis, id)
            if resultadoQ == 0:
                print("No se encontró el elemento solicitado")
            else:
                list(map(lambda x: [x.setUsuario(usuario), x.setAnimal(animal), x.setEnfemedad(enfermedad),
                                    x.setPeso(peso), x.setDosis(idDosis)]
                                    if x.getID() == id else ' ', generalPrescripciones))

def Eliminar(stringTabla, request):
    nombreAEM = request.form["nombre"]
    global listaAEM
    global generalAEM
    tempDosis = list(filter(lambda x: x.getAnimal() == nombreAEM
        or x.getMedicamento() == nombreAEM or x.getEnfermedad() == nombreAEM,generalDosis))
    if (len(tempDosis) >0):
        print("No se puede eliminar ese elemento, pues está asociado a una dosis.")
    else:
        tempCantidad = len(listaAEM)
        listaAEM = list(filter(lambda x: not(x.getNombre() == nombreAEM and x.getClase() == stringTabla),listaAEM))
        if (len(listaAEM == tempCantidad)):
            #No cambio la lista temporal, toca buscar en la BD
            resultadoQ = EliminarBD(stringTabla,nombreAEM)
            if resultadoQ == 0:
                print("No se realizó ningun cambio, compruebe los datos")
            else:
                generalAEM = list(
                    filter(lambda x: not (x.getNombre() == nombreAEM and x.getClase() == stringTabla), generalAEM))
        else:
            generalAEM = list(filter(lambda x: not(x.getNombre() == nombreAEM and x.getClase() == stringTabla),generalAEM))

def EliminarUsuario(request):
    usuario = request.form["usuario"]
    global listaUsuarios
    global generalUsuarios
    tempPresc = list(filter(lambda x: x.getUsuario() == usuario,generalPrescripciones))
    if len(tempPresc) > 0:
        print("No se puede eliminar el usuario, ya que está asociado a alguna prescripción")
    else:
        tempCantidad = len(listaUsuarios)
        listaUsuarios = list(filter(lambda x: x.getLogin() == usuario, listaAEM))
        if (len(listaAEM == tempCantidad)):
            # No cambio la lista temporal, toca buscar en la BD
            resultadoQ = EliminarUsuarioBD(usuario)
            if resultadoQ == 0:
                print("No se realizó ningun cambio, compruebe los datos")
            else:
                generalUsuarios = list(filter(lambda x: x.getLogin() == usuario, generalUsuarios))
        else:
            generalUsuarios = list(filter(lambda x: x.getLogin() == usuario, generalUsuarios))

def EliminarDosis(request):
    idDosis = request.form['idDosis']
    global listaDosis
    global generalDosis
    tempPresc = list(filter(lambda x: x.getDosis() == idDosis, generalPrescripciones))
    if len(tempPresc) > 0:
        print("No se puede eliminar la dosis, ya que está asociada a alguna prescripción")
    else:
        tempCantidad = len(listaDosis)
        listaDosis = list(filter(lambda x: x.getID() == idDosis, listaDosis))
        if (len(listaDosis == tempCantidad)):
            # No cambio la lista temporal, toca buscar en la BD
            resultadoQ = EliminarDosisBD(idDosis)
            if resultadoQ == 0:
                print("No se realizó ningun cambio, compruebe los datos")
            else:
                generalDosis = list(filter(lambda x: x.getID() == idDosis, generalDosis))
        else:
            generalDosis = list(filter(lambda x: x.getID() == idDosis, generalDosis))

def EliminarPrescripcion(request):
    idPresc = request.form['idPrescripcion']
    global listaPrescripciones
    global generalPrescripciones
    tempCantidad = len(listaPrescripciones)
    listaPrescripciones = list(filter(lambda x: x.getID() == idPresc, listaPrescripciones))
    if (len(listaPrescripciones == tempCantidad)):
        # No cambio la lista temporal, toca buscar en la BD
        resultadoQ = EliminarPrescripcionBD(idPresc)
        if resultadoQ == 0:
            print("No se realizó ningun cambio, compruebe los datos")
        else:
            generalPrescripciones = list(filter(lambda x: x.getID() == idPresc, generalPrescripciones))
    else:
        generalPrescripciones = list(filter(lambda x: x.getID() == idPresc, generalPrescripciones))

def GuardarCambios():
    global contador
    list(map(lambda x: [InsertarBD(gAEM.__next__().getClase(),gAEM.__next__().getNombre(),
                                  gAEM.__next__().getDescripcion(), gAEM.__next__().getFoto()),
                                  AumentarContador()],range(len(listaAEM))))
    contador = 0
    list(map(lambda x: [insertarUsuarioBD(gUsuarios.__next__().getLogin(),gUsuarios.__next__().getPassword(),
                                  gUsuarios.__next__().getNombre(), gUsuarios.__next__().getPermiso(),
                                  gUsuarios.__next__().getFoto()),AumentarContador()],range(len(listaUsuarios))))
    contador = 0
    list(map(lambda x: [InsertarDosisBD(gDosis.__next__().getID(), gDosis.__next__().getAnimal(),
                                  gDosis.__next__().getMedicamento(), gDosis.__next__().getEnfermedad(),
                                  gDosis.__next__().getMinPeso(),gDosis.__next__().getMaxPeso(),
                                  gDosis.__next__().getDosis()),AumentarContador()],range(len(listaDosis))))
    contador = 0
    list(map(lambda x: [InsertarPrescripcionBD(gPresc.__next__().getID(), gPresc.__next__().getUsuario(),
                                              gPresc.__next__().getAnimal(), gPresc.__next__().getEnfermedad(),
                                              gPresc.__next__().getPeso(), gPresc.__next__().getDosis()),AumentarContador()],
                                              range(len(listaPrescripciones))))
    contador = 0
    CargarListasGenerales()
    LimpiarListasLocales()
    print("Se han guardado todos los cambios! ")

# u1 = Usuario()
# u1.setLogin("Car")
# u1.setPassword(123)
# u1.setNombre("Carlos Villafuerte")
# u1.setPermiso("admin")
# u1.setFoto("assdadsa")
# a1 = Animal()
# a1.setNombre("Lobo")
# a1.setDescripcion("Ladra")
# a1.setFoto("asddsa")
# a2 = Animal()
# a2.setNombre("Leon")
# a2.setDescripcion("Maulla")
# a2.setFoto("dasasdd")
# e1 = Enfermedad()
# e1.setNombre("Distemper")
# e1.setDescripcion("asdasdsa")
# e1.setFoto("asddsaads")
# m1 = Medicamento()
# m1.setNombre("Paracetamol")
# m1.setDescripcion("asddsa")
# m1.setFoto("adasd")
# d1 = Dosis()
# d1.setID(4)
# d1.setAnimal("Perro")
# d1.setEnfermedad("Distemper")
# d1.setMedicamento("Paracetamol")
# d1.setRangoPeso(8,15)
# d1.setDosis(13)
# p1 = Prescripcion()
# p1.setID(2)
# p1.setUsuario("Car")
# p1.setAnimal("Lobo")
# p1.setEnfermedad("Distemper")
# p1.setPeso(10)
# p1.setDosis(4)
# listaAEM.append(a1)
# listaAEM.append(a2)
# listaAEM.append(e1)
# listaAEM.append(m1)
# print(range(len(listaAEM)))
# listaUsuarios.append(u1)
# listaDosis.append(d1)
# listaPrescripciones.append(p1)
#
# GuardarCambios()
