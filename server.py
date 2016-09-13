from flask import Flask,request,render_template,jsonify,redirect, url_for # Esta siempre va en proyectos de flask
from flask import make_response
from werkzeug.utils import secure_filename
from manager import *
import base64
from DTO import *
from Conexion import *

UPLOAD_FOLDER = 'imagenesUsuario'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpe', 'jpeg', 'gif'])
usuarioAdentro = Usuario

filtroActivo = False

listaAn = []
listaMe = []
listaPr = []
lista_Do_Fi = []
lista_Do_Ge = []
cantPagAn = 0
cantPagPr = 0
cantPagMe = 0
cantPagDo = 0
cantPag_Do_Fi_An = 0
cantPag_Do_Fi_En = 0


app = Flask(__name__)  # Instancia para llamar a los routers.
app.secret_key = 'some_secret'


@app.route('/')
def index():
    'Pinta la pagina principal, un login.'
    return render_template("login.html")

@app.route('/profileUser', methods=['GET', 'POST'])
def profileUser():
    """ Valida la entrada de un usuario al sistema.
    recibe le nombre y la contraseña del usuario y retorna
    el objeto con ese usuario.
    :parameter
        nombreUsuario: Nombre del usuario
        contasena: Contraseña del usuario.

    """
    global usuarioAdentro
    if request.method == 'POST':
        nombreUsuario = request.form['nombreUsuario']
        contrasena = request.form['contrasena']
        usuario = obtenerUsuarioManager(str(nombreUsuario), str(contrasena))

        usuarioAdentro = usuario
        if usuario == "error":
            return render_template("login.html", suceso="¡¡ No existe ese usuario !!")
        elif(usuario.getPermiso() == "admin"):
            resultado = "data:image/jpeg;base64," + usuario.getFoto().decode('utf8')
            usuarioAdentro.setFoto(resultado)
            #usuarioAdentro.setFotoDecodificada(resultado)
            return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuario)
        elif(usuario.getPermiso() == "normal"):
            resultado = "data:image/jpeg;base64," + usuario.getFoto().decode('utf8')
            usuarioAdentro.setFoto(resultado)
            return render_template("usuarioAdmin/usuarioNormal.html", usuario=usuario)
    else:
        if(usuarioAdentro.getPermiso() == "admin"):
            return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro)
        elif(usuarioAdentro.getPermiso() == "normal"):
            return render_template("usuarioAdmi.html", usuario=usuarioAdentro)


def allowed_file(filename):
    """Verifica que el archvo subido tenga extención de imagen"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    suceso = ""
    opcion = request.form["submit"]
    if opcion == "modificar":
        suceso = ModificarUsuario(request)
    elif opcion == "eliminar":
        suceso = EliminarUsuario(request)
    else:
        """Obtiene los datos de un usuario nuevo, llama a metodos de manager
        para guardarlos en la lista hasta que este listo para insertarse en la BD."""
        if 'foto' not in request.files:
            render_template("login.html", suceso="¡¡ No subio la foto !!")
        # nombreCompleto = request.form['nombreCompleto']
        # usuario = request.form['usuario']
        # contrasena = request.form['contrasena']
        # permiso = request.form['permiso']
        foto = request.files['foto']
        # valor = base64.b64encode(foto.getvalue())
        # resultado = valor.decode('utf8')
        if foto.filename == '':
            render_template("login.html", suceso="¡¡ No subio la foto !!")
        if foto and allowed_file(foto.filename):
             filename = secure_filename(foto.filename)
             # InsertarUsuarioManager1(usuario, contrasena, nombreCompleto, permiso, resultado)
             suceso = InsertarUsuario(request)#Retorna lo que paso!
    return render_template("login.html", suceso=suceso)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    """Agrega,modifica y elimina los medicamentos/animales/enfermedades a las listas respectivas,
    llama a una función generica en manager, para cada opcion agregar/modi... """
    global usuarioAdentro
    opcion = request.form['submit']
    categoria = request.form['categoria']
    if opcion == "eliminar":
        suceso = Eliminar(categoria, request)
        return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso=suceso)
    else:
        if request.files['foto'].filename == '':
            return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso="No viene la foto")
        if request.files['foto'] and allowed_file(request.files['foto'].filename):
            if opcion == "agregar":
                if categoria == "Medicamento":
                    suceso = InsertarManager(Medicamento, request)
                elif categoria == "Animal":
                    suceso = InsertarManager(Animal, request)
                elif categoria == "Enfermedad":
                    suceso = InsertarManager(Enfermedad, request)
                return render_template("usuarioAdmin/usuarioAdmi.html", suceso=suceso, usuario=usuarioAdentro)
            elif opcion == "modificar":
                suceso = Modificar(categoria, request)
                return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso=suceso)

@app.route('/agregarDosis', methods=['GET', 'POST'])
def agregarDosis():
    global usuarioAdentro
    opcion = request.form['submit']
    suceso = "Ha ocurrido un error..."
    if opcion == "agregar":
        suceso = InsertarDosis(request)
    elif opcion == "modificar":
        suceso = ModificarDosis(request)
    elif opcion == "eliminar":
        suceso = EliminarDosis(request)
    return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso=suceso)


@app.route('/agregarPrescripcion', methods=['GET', 'POST'])
def agregarPrescripcion():
    """Hace un llamado a la funcion de agregar prescipciones en manager
    manda por parametros los datos recolectados.
    """
    global usuarioAdentro
    sigVista = ""
    if usuarioAdentro.getPermiso() == "admin":
        sigVista = "usuarioAdmin/usuarioAdmi.html"
    else:
        sigVista = "usuarioAdmin/usuarioNormal.html"
    opcion = request.form['submit']
    suceso = "Ha ocurrido un error..."
    if "getID" != opcion:
        if opcion == "agregar":
            suceso = InsertarPrescripcion(request)
        elif opcion == "modificar":
            suceso = ModificarPrescripcion(request)
        elif opcion == "eliminar":
            suceso = EliminarPrescripcion(request)
        return render_template(sigVista, usuario=usuarioAdentro, suceso=suceso)
    else:
        idPresc = request.form["idPrescripcion"]
        animal = request.form['animal']
        enfermedad = request.form['enfermedad']
        peso = request.form['peso']
        idDosis = ObtenerIdDosis(request)
        if idDosis != "error":
            return render_template(sigVista, usuario=usuarioAdentro,
                               suceso="Se recupero el ID: "+str(idDosis[0].getID()), idPresc = idPresc,
                               animal=animal, enfermedad=enfermedad, peso=peso, idDosis=idDosis[0].getID())
        else:
            return render_template(sigVista, usuario=usuarioAdentro,
                                   suceso="¡¡ No existe en la Base de Datos !!")


@app.route('/listarAnimales', methods=['GET', 'POST'])
def listarAnimales():
    global cantPagAn
    if len(listaAn) == 0:
        resultado = ObtenerAEM("Animal")
        if resultado == "error":
            return render_template("vistasDeListados/listadoAnimales.html", data=resultado)
        if len(resultado)%10 != 0:
            cantPagAn = (len(resultado) // 10) + 2
        else:
            cantPagAn = len(resultado) % 10 + 1
        listaAn.extend(resultado)
    if len(listaAn) <= 10:
        listaTemp = []
        listaTemp.extend(listaAn)
        listaAn.clear()
        return render_template("vistasDeListados/listadoAnimales.html", data=listaTemp, paginas=cantPagAn)
    else:
        listaPri10 = []
        listaPri10.extend(listaAn[:10])
        listaResto = []
        listaResto.extend(listaAn[10:])
        listaAn.clear()
        listaAn.extend(listaResto)
        return render_template("vistasDeListados/listadoAnimales.html", data=listaPri10, paginas=cantPagAn)


@app.route('/listarMedicinas', methods=['GET', 'POST'])
def listarMedicamentos():
    global cantPagMe
    if len(listaMe) == 0:
        resultado = ObtenerAEM("Medicamento")
        for i in resultado:
            print(i.getNombre())
        if resultado == "error":
            return render_template("vistasDeListados/listadoMedicinas.html", data=resultado)
        if len(resultado)%10 != 0:
            cantPagMe = (len(resultado) // 10) + 2
        else:
            cantPagMe = len(resultado) % 10 + 1
        listaMe.extend(resultado)
    if len(listaMe) <= 10:
        listaTemp = []
        listaTemp.extend(listaMe)
        listaMe.clear()
        return render_template("vistasDeListados/listadoMedicinas.html", data=listaTemp, paginas=cantPagMe)
    else:
        listaPri10 = []
        listaPri10.extend(listaMe[:10])
        listaResto = []
        listaResto.extend(listaMe[10:])
        listaMe.clear()
        listaMe.extend(listaResto)
        return render_template("vistasDeListados/listadoMedicinas.html", data=listaPri10, paginas=cantPagMe)


@app.route('/listarPrescripciones', methods=['GET', 'POST'])
def listarEnfermedades():
    global cantPagPr
    if len(listaPr) == 0:
        resultado = ObtenerPrescripcion()
        if resultado == "error":
            return render_template("vistasDeListados/listadoPrescripcion.html", data=resultado)
        print(resultado)
        if len(resultado) % 10 != 0:
            cantPagPr = (len(resultado) // 10) + 2
        else:
            cantPagPr = len(resultado) % 10 + 1
        listaPr.extend(resultado)
    if len(listaPr) <= 10:
        listaTemp = []
        listaTemp.extend(listaPr)
        listaPr.clear()
        return render_template("vistasDeListados/listadoPrescripcion.html", data=listaTemp, paginas=cantPagPr)
    else:
        listaPri10 = []
        listaPri10.extend(listaPr[:10])
        listaResto = []
        listaResto.extend(listaPr[10:])
        listaPr.clear()
        listaPr.extend(listaResto)
        return render_template("vistasDeListados/listadoPrescripcion.html", data=listaPri10, paginas=cantPagPr)


@app.route('/listarDosis', methods=['GET', 'POST'])
def listarDosis():
    global cantPag_Do_Fi_An
    global filtroActivo
    if request.method == 'POST':
        resultado = ObternerFiltroDosis(request)
        print("Server")
        print(resultado)
        if resultado == "error":
            return render_template("vistasDeListados/listadoDosis.html", data=resultado)
        if len(resultado) % 10 != 0:
            cantPag_Do_Fi_An = (len(resultado) // 10) + 2
        else:
            cantPag_Do_Fi_An = len(resultado) % 10 + 1
        lista_Do_Fi.extend(resultado)
        filtroActivo = True
        if len(lista_Do_Fi) <= 10:
            listaTemp = []
            listaTemp.extend(lista_Do_Fi)
            lista_Do_Fi.clear()
            filtroActivo = False
            return render_template("vistasDeListados/listadoDosis.html", data=listaTemp, paginas=cantPag_Do_Fi_An)
        else:
            listaPri10 = []
            listaPri10.extend(lista_Do_Fi[:10])
            listaResto = []
            listaResto.extend(lista_Do_Fi[10:])
            lista_Do_Fi.clear()
            lista_Do_Fi.extend(listaResto)
            return render_template("vistasDeListados/listadoDosis.html", data=listaPri10, paginas=cantPag_Do_Fi_An)
    if filtroActivo == True:
        if len(lista_Do_Fi) <= 10:
            listaTemp = []
            listaTemp.extend(lista_Do_Fi)
            lista_Do_Fi.clear()
            filtroActivo = False
            return render_template("vistasDeListados/listadoDosis.html", data=listaTemp, paginas=cantPag_Do_Fi_An)
        else:
            listaPri10 = []
            listaPri10.extend(lista_Do_Fi[:10])
            listaResto = []
            listaResto.extend(lista_Do_Fi[10:])
            lista_Do_Fi.clear()
            lista_Do_Fi.extend(listaResto)
            return render_template("vistasDeListados/listadoDosis.html", data=listaPri10, paginas=cantPag_Do_Fi_An)
    if len(lista_Do_Ge) == 0:
        resultado = ObtenerDosis()
        if resultado == "error":
            return render_template("vistasDeListados/listadoDosis.html", data=resultado)
        if len(resultado) % 10 != 0:
            cantPag_Do_Fi_An = (len(resultado) // 10) + 2
        else:
            cantPag_Do_Fi_An = len(resultado) % 10 + 1
        lista_Do_Ge.extend(resultado)
    if len(lista_Do_Ge) <= 10:
        listaTemp = []
        listaTemp.extend(lista_Do_Ge)
        lista_Do_Ge.clear()
        return render_template("vistasDeListados/listadoDosis.html", data=listaTemp, paginas=cantPag_Do_Fi_An)
    else:
        listaPri10 = []
        listaPri10.extend(lista_Do_Ge[:10])
        listaResto = []
        listaResto.extend(lista_Do_Ge[10:])
        lista_Do_Ge.clear()
        lista_Do_Ge.extend(listaResto)
        return render_template("vistasDeListados/listadoDosis.html", data=listaPri10, paginas=cantPag_Do_Fi_An)

@app.route('/ObtenerAEM', methods=['GET', 'POST'])
def ObtenerInfoAEM():
    """"""
    tipo = request.args.get('tipo')
    objeto = ObtenerDatosAEM(tipo,request.args.get('nombre'))
    return render_template("vistasDeListados/datosAEM.html", tipo=tipo, objeto=objeto)


@app.route('/agregarBD')
def agregarBD():
    """Agrega todos los datos recolectados en las listas temporales a la base de datos
    :parameter
        None
    :returns
        El estado de la inserción en la base de datos
    """
    global usuarioAdentro
    suceso = GuardarCambios()
    if (usuarioAdentro.getPermiso() == "admin"):
        return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso=suceso)
    elif (usuarioAdentro.getPermiso() == "normal"):
        return render_template("usuarioAdmin/usuarioNormal.html", usuario=usuarioAdentro, suceso=suceso)


#Para agregar el usuario al inicio, solo al inicio
@app.route('/register', methods=['GET','POST'])
def register():
    """Para agregar el usuario directamente a la base de datos, sin pasar por las restrinciones
    :parameter
        El request con los datos del usuario.
    :returns
        el estado de la insercion en la BD.
    """
    if 'foto' not in request.files:
        return redirect(request.url)
    usuario = request.form["usuario"]
    contrasena = request.form['contrasena']
    nombreCompleto = request.form['nombreCompleto']
    permiso = request.form['permiso']
    foto = request.files['foto']
    valor = base64.b64encode(foto.getvalue())
    resultado = valor.decode('utf8')
    if foto.filename == '':
        return redirect(request.url)
    if foto and allowed_file(foto.filename):
        filename = secure_filename(foto.filename)
    insertarUsuarioBD(usuario, contrasena, nombreCompleto, permiso, resultado)
    return render_template("login.html")



# Esto lo hace correr. El debug = true permite que se impriman los errores, si se quita igual funciona

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)