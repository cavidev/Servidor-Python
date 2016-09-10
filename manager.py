import base64
from Conexion import *
from DTO import *
from flask import request

# Listas Temporales
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

    tempLista = list(filter(lambda x: x.getID() == id, generalPrescripciones))
    if len(tempLista) > 0:
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
    for i in listaAEM:
        if i.getClase() == "Animal":
            print(i.getNombre(), i.getDescripcion(), i.getFoto())
