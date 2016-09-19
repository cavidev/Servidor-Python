import base64
from Conexion import *
from DTO import *
from flask import request

# Listas Temporales
listaAEM = []
listaUsuarios = []
listaDosis = []
listaPrescripciones = []

def LimpiarListas():
    listaAEM.clear()
    listaUsuarios.clear()
    listaDosis.clear()
    listaPrescripciones.clear()
    generalAEM.clear()
    generalUsuarios.clear()
    generalDosis.clear()
    generalPrescripciones.clear()

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
    """Generador de la lista de Animales,Enfermedad/Medicina
    devuelve una llamana en yield de lo solicitado."""
    global contador
    while True:
        yield listaAEM[contador]


def generadorUsuarios():
    """Usando generador, devuelve cada objeto de tipo usuario."""
    global contador
    while True:
        yield listaUsuarios[contador]


def generadorDosis():
    """Devuelve el obejto dosis."""
    global contador
    while True:
        yield listaDosis[contador]

def generadorPrescripciones():
    """Devuelve el objeto de las prescripciones."""
    global contador
    while True:
        yield listaPrescripciones[contador]

gAEM = generadorAEM()
gUsuarios = generadorUsuarios()
gDosis = generadorDosis()
gPresc = generadorPrescripciones()


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
        nuevoObjeto.setFoto(resultado)
        listaUsuarios.append(nuevoObjeto)
        generalUsuarios.append(nuevoObjeto)
        return "¡¡ Se agrego a la lista de espera !!"


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
    nuevoObjeto.setFoto(resultado)
    if len(list(filter(lambda x: x.getNombre() == request.form['nombre'],generalAEM))):
        return "¡¡ Ya existe algo con ese ID!!"
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
        tempDosis = list(filter(lambda z: str(z.getID()) == idDosis, generalDosis))
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


def InsertarUsuarioManager1(login, password, nombre, permiso, foto):
    'Inserta el usuario directamente en la BD.'
    return insertarUsuarioBD(login, password, nombre, permiso, foto)


def Modificar(stringTabla, request):
    """Modifica cualquiera de las 3 tablas; anim,enfe,medici.Con los atributos
    requeridos por el usuario.
    :parameter
        stringTabla: nombre de la tabla a modificar
        request: datos enviados por el usuario
    :returns
        El estado de la modificación."""
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
        resultadoQ = ModificarBD(stringTabla, nuevaDesc, nuevaFoto, nombre)
        if resultadoQ == 0:
            return "¡¡ No se encontró el elemento solicitado !!"
        else:
            list(map(lambda x: [x.setDescripcion(nuevaDesc),
                                x.setFoto(nuevaFoto)] if x.getClase() == stringTabla and x.getNombre() == nombre else ' ',
                                generalAEM))
        return "¡¡ Se modifico con exito!!"


def ModificarUsuario(request):
    """Modifica la informacion de un usuario en la base de datos,
    :parameter
        request: datos enviado por los usuarios.
    :returns
        El estado de la modificacion"""
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
            return "No hubieron cambios, datos incorrectos o repetidos."
        else:
            list(map(lambda x: [x.setPassword(contra), x.setNombre(nombreCompleto), x.setPermiso(permiso),
                                x.setFoto(resultado)] if x.getLogin() == usuario else ' ', generalUsuarios))
    return "Modificación exitosa!"


def ModificarDosis(request):
    """Modifica la dosis existentes.
    :parameter
        request: Datos enviados por el usuario
    :returns
        El estado de la modificacion.
    """

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
            list(map(lambda x: [x.setAnimal(animal), x.setMedicamento(medicamento), x.setEnfermedad(enfermedad),
                                x.setRangoPeso(minPeso,maxPeso), x.setDosis(dosis)]
                                if x.getID() == id else ' ', listaDosis))
            list(map(lambda x: [x.setAnimal(animal), x.setMedicamento(medicamento), x.setEnfermedad(enfermedad),
                                x.setRangoPeso(minPeso, maxPeso), x.setDosis(dosis)]
                                if x.getID() == id else ' ', generalDosis))
        else:
            resultadoQ = ModificarDosisBD(animal,medicamento,enfermedad,minPeso,maxPeso,dosis,id)
            if resultadoQ == 0:
                return "No se encontró el elemento solicitado"
            else:
                list(map(lambda x: [x.setAnimal(animal), x.setMedicamento(medicamento), x.setEnfermedad(enfermedad),
                                    x.setRangoPeso(minPeso, maxPeso), x.setDosis(dosis)]
                                    if x.getID() == id else ' ', generalDosis))
    return "Modificación exitosa!"


def ModificarPrescripcion(request):
    """Modifica las prescripciones existentes en la base de datos.
    :parameter
        request: Datos enviados por los usuarios
    :returns
        El estado de la insercion."""
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
    tempDosis = list(filter(lambda z: str(z.getID()) == idDosis, generalDosis))

    if len(tempAEM) != 2 or len(tempUsuario) != 1 or len(tempDosis) != 1:
        return "¡¡ No se encontraron los datos solicitados !!"
    else:
        if len(list(filter(lambda x: x.getID() == id, generalPrescripciones))) > 0:
            list(map(lambda x: [x.setUsuario(usuario),x.setAnimal(animal),x.setEnfermedad(enfermedad),
                                x.setPeso(peso),x.setDosis(idDosis)]
                                if x.getID() == id else ' ', listaPrescripciones))
            list(map(lambda x: [x.setUsuario(usuario), x.setAnimal(animal), x.setEnfermedad(enfermedad),
                                x.setPeso(peso), x.setDosis(idDosis)]
                                if x.getID() == id else ' ', generalPrescripciones))
        else:
            resultadoQ = ModificarPrescripcionBD(usuario, animal, enfermedad,peso, idDosis, id)
            if resultadoQ == 0:
                return "No se encontró el elemento solicitado"
            else:
                list(map(lambda x: [x.setUsuario(usuario), x.setAnimal(animal), x.setEnfermedad(enfermedad),
                                    x.setPeso(peso), x.setDosis(idDosis)]
                                    if x.getID() == id else ' ', generalPrescripciones))
    return "Modificación exitosa!"


def obtenerUsuarioManager(login, contrasena):
    """Obtien el usuario que se esta logeando,
    Parametros:
        login: Nombre de usuario
        contrasena: La contraseña del usuario.
    Returns:
        Usuario if encuentra else estado de la busqueda."""
    listaGenerada = list(
        filter(lambda x: x.getLogin() == login and x.getPassword() == contrasena, generalUsuarios))
    if 0 < len(listaGenerada):
        return listaGenerada[0]
    else:
        return "error"


def ObtenerAEM(filtro):
    """Retorna una lista con los animales de toda la BD,
    usa una función lambda
    :parameter
        filtro: el nombre del requerimiento del cliente.
    :returns
        El estado del filtro, lista o el error.
        """
    lista = list(filter(lambda x: x.getClase() == filtro, generalAEM))
    if 0 < len(lista):
        return lista
    else:
        return "error"


def ObtenerIdDosis(request):
    """Obtiene le ID de una dosis especificada por el usuario.
    :parameter
        request: Datos solicitados por el usuario.
    :returns
        ID: el resultado de la busqueda."""
    animal = request.form['animal']
    enfermedad = request.form['enfermedad']
    peso = request.form['peso']
    listaTemp = list(filter(lambda x: x.getAnimal() == animal and x.getEnfermedad() == enfermedad
                            and (int(x.getMinPeso()) <= int(peso) < int(x.getMaxPeso())), generalDosis))
    if len(listaTemp) > 0:
        return listaTemp
    else:
        return "error"


def ObtenerDosis():
    """Retorna todas las docis que estan las lista generale osea en la BD
    :parameter
        None
    :returns
        La lista obtenida o el error.
        """
    if len(generalDosis) > 0:
        return generalDosis
    else:
        return "error"


def ObtenerPrescripcion():
    """Obtiene las prescriciones de las listas generales
    :parameter
        None
    :returns
        La lista con las prescripciones o el error
        """
    if len(generalPrescripciones) > 0:
        return generalPrescripciones
    else:
        return "error"


def ObternerFiltroDosis(request):
    """Retorna la dosis por el filtro que el usuario desee, en cual viene por parametro.
    :parameter
        request: la solicitud del usuario.
    :returns
        La lista con el filtro hecho.
        """
    pedido = request.form['pedido']
    opcion = request.form['submit']
    if "Animal" == opcion:
        lista = list(filter(lambda x: x.getAnimal() == pedido, generalDosis))
        if len(lista) > 0:
            return lista
        else:
            return "error"
    else:
        lista = list(filter(lambda x: x.getEnfermedad() == pedido, generalDosis))
        if len(lista) > 0:
            return lista
        else:
            return "error"


def ObtenerDatosAEM(tipo,nombre):
    """Obtiene el objeto con solicitado por el usuario
    :parameter
        tipo: tipo de dato solicitado
        nombre: nombre del filtro a hacer.
    :returns
        el objeto else el estado de error."""
    lista = list(filter(lambda x: x.getClase() == tipo and x.getNombre() == nombre, generalAEM))
    if 0 < len(lista):
        return lista[0]
    else:
        return "error"


def Eliminar(stringTabla, request):
    """Elimina de la listas generales el objeto que le usuario envie por parametro
     :parameter
        stringTable: El nombre de la tabla que se desea borrar
        request: El nombre del atributo que se quiere borrar.
    :returns
        El estado de la eliminacion"""
    nombreAEM = request.form["nombre"]
    global listaAEM
    global generalAEM
    tempDosis = list(filter(lambda x: x.getAnimal() == nombreAEM
        or x.getMedicamento() == nombreAEM or x.getEnfermedad() == nombreAEM, generalDosis))
    if (len(tempDosis) > 0):
        return "¡¡ No se puede eliminar ese elemento, pues está asociado a una dosis. !!"
    else:
        tempCantidad = len(listaAEM)
        listaAEM = list(filter(lambda x: not(x.getNombre() == nombreAEM and x.getClase() == stringTabla),listaAEM))
        if (len(listaAEM) == tempCantidad):
            #No cambio la lista temporal, toca buscar en la BD
            resultadoQ = EliminarBD(stringTabla, nombreAEM)
            if resultadoQ == 0:
                return "¡¡ No se realizó ningun cambio, compruebe los datos !!"
            else:
                generalAEM = list(
                    filter(lambda x: not (x.getNombre() == nombreAEM and x.getClase() == stringTabla), generalAEM))
        else:
            generalAEM = list(filter(lambda x: not(x.getNombre() == nombreAEM and x.getClase() == stringTabla), generalAEM))
    return "Se eliminó con éxito"


def EliminarUsuario(request):
    """Elimina de la listas generales el objeto que le usuario envie por parametro
     :parameter
        request: El nombre del atributo que se quiere borrar.
    :returns
        El estado de la eliminacion"""
    usuario = request.form["usuario"]
    global listaUsuarios
    global generalUsuarios
    tempPresc = list(filter(lambda x: x.getUsuario() == usuario,generalPrescripciones))
    if len(tempPresc) > 0:
        return "No se puede eliminar el usuario, ya que está asociado a alguna prescripción"
    else:
        tempCantidad = len(listaUsuarios)
        listaUsuarios = list(filter(lambda x: x.getLogin() != usuario, listaAEM))
        if (len(listaAEM) == tempCantidad):
            # No cambio la lista temporal, toca buscar en la BD
            resultadoQ = EliminarUsuarioBD(usuario)
            if resultadoQ == 0:
                return "No se realizó ningun cambio, compruebe los datos"
            else:
                generalUsuarios = list(filter(lambda x: x.getLogin() != usuario, generalUsuarios))
        else:
            generalUsuarios = list(filter(lambda x: x.getLogin() != usuario, generalUsuarios))
    return "El usuario "+ usuario + " se eliminó exitosamente"


def EliminarDosis(request):
    """Elimina de la listas generales el objeto que le usuario envie por parametro
     :parameter
        request: El nombre del atributo que se quiere borrar.
    :returns
        El estado de la eliminacion"""
    idDosis = request.form['idDosis']
    global listaDosis
    global generalDosis
    tempPresc = list(filter(lambda x: x.getDosis() == idDosis, generalPrescripciones))
    if len(tempPresc) > 0:
        return "No se puede eliminar la dosis, ya que está asociada a alguna prescripción"
    else:
        tempCantidad = len(listaDosis)
        listaDosis = list(filter(lambda x: x.getID() != idDosis, listaDosis))
        if (len(listaDosis) == tempCantidad):
            # No cambio la lista temporal, toca buscar en la BD
            resultadoQ = EliminarDosisBD(idDosis)
            if resultadoQ == 0:
                return "No se realizó ningun cambio, compruebe los datos"
            else:
                generalDosis = list(filter(lambda x: x.getID() != idDosis, generalDosis))
        else:
            generalDosis = list(filter(lambda x: x.getID() != idDosis, generalDosis))
        return "Se eliminó exitosamente"


def EliminarPrescripcion(request):
    """Elimina de la listas generales el objeto que le usuario envie por parametro
     :parameter
        request: El nombre del atributo que se quiere borrar.
    :returns
        El estado de la eliminacion"""
    idPresc = request.form['idPrescripcion']
    global listaPrescripciones
    global generalPrescripciones
    tempCantidad = len(listaPrescripciones)
    listaPrescripciones = list(filter(lambda x: x.getID() != idPresc, listaPrescripciones))
    if (len(listaPrescripciones) == tempCantidad):
        # No cambio la lista temporal, toca buscar en la BD
        resultadoQ = EliminarPrescripcionBD(idPresc)
        if resultadoQ == 0:
            return "No se realizó ningun cambio, compruebe los datos"
        else:
            generalPrescripciones = list(filter(lambda x: x.getID() != idPresc, generalPrescripciones))
    else:
        generalPrescripciones = list(filter(lambda x: x.getID() != idPresc, generalPrescripciones))
    return "Se eliminó exitosamente"


def GuardarCambios():
    """Guardas todos los cambios hechos en las listas a la base de datos, llama a funciones localizadas en conexion.py
    :parameter
        None
    :returns
        El estado de la insercion en la base de datos."""
    global contador
    list(map(lambda x: [InsertarBD(gAEM.__next__().getClase(), gAEM.__next__().getNombre(),
                                  gAEM.__next__().getDescripcion(), gAEM.__next__().getFoto()),
                                  AumentarContador()], range(len(listaAEM))))
    contador = 0
    list(map(lambda x: [insertarUsuarioBD(gUsuarios.__next__().getLogin(), gUsuarios.__next__().getPassword(),
                                  gUsuarios.__next__().getNombre(), gUsuarios.__next__().getPermiso(),
                                  gUsuarios.__next__().getFoto()), AumentarContador()], range(len(listaUsuarios))))
    contador = 0
    list(map(lambda x: [InsertarDosisBD(gDosis.__next__().getID(), gDosis.__next__().getAnimal(),
                                  gDosis.__next__().getMedicamento(), gDosis.__next__().getEnfermedad(),
                                  gDosis.__next__().getMinPeso(), gDosis.__next__().getMaxPeso(),
                                  gDosis.__next__().getDosis()), AumentarContador()], range(len(listaDosis))))
    contador = 0
    list(map(lambda x: [InsertarPrescripcionBD(gPresc.__next__().getID(), gPresc.__next__().getUsuario(),
                                              gPresc.__next__().getAnimal(), gPresc.__next__().getEnfermedad(),
                                              gPresc.__next__().getPeso(), gPresc.__next__().getDosis()), AumentarContador()],
                                              range(len(listaPrescripciones))))
    contador = 0
    LimpiarListas()
    CargarListasGenerales()
    return "¡¡ Se han guardado todos los cambios!! "
