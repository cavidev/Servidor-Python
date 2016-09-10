import os
from flask import Flask,request,render_template,jsonify,redirect, url_for # Esta siempre va en proyectos de flask
from flask import make_response
from werkzeug.utils import secure_filename
from manager import *
import base64
from DTO import *

UPLOAD_FOLDER = 'imagenesUsuario'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpe','jpeg', 'gif'])
usuarioAdentro = Usuario

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
    nombreUsuario = request.form['nombreUsuario']
    contrasena = request.form['contrasena']
    usuario = obtenerUsuarioManager(str(nombreUsuario), str(contrasena))
    global usuarioAdentro
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
        return render_template("usuarioAdmi.html", usuario=usuario)


def allowed_file(filename):
    """Verifica que el archvo subido tenga extención de imagen"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/registerUser', methods=['GET','POST'])
def registerUser():
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


@app.route('/agregar', methods=['GET','POST'])
def agregar():
    """Agrega,modifica y elimina los medicamentos/animales/enfermedades a las listas respectivas,
    llama a una función generica en manager, para cada opcion agregar/modi... """
    global usuarioAdentro
    if request.files['foto'].filename == '':
        return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso="No viene la foto")
    if request.files['foto'] and allowed_file(request.files['foto'].filename):
        opcion = request.form['submit']
        categoria = request.form['categoria']
        if opcion == "agregar":
            if categoria == "Medicamento":
                suceso = InsertarManager(Medicamento, request)
            elif categoria == "Animal":
                print("Llego al server")
                suceso = InsertarManager(Animal, request)
            elif categoria == "Enfermedad":
                suceso = InsertarManager(Enfermedad, request)
            return render_template("usuarioAdmin/usuarioAdmi.html", suceso=suceso, usuario=usuarioAdentro)
        elif opcion == "modificar":
            if categoria == "Medicamento":
                print("Modificar")
                #ModificarManager(Medicamento, request)
            elif categoria == "Animal":
                print("Modificar")
                # ModificarManager(Animal, request)
            elif categoria == "Enfermedad":
                print("Modificar")
                #ModificarManager(Enfermedad, request)
            return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso="Se modifico: ")
        elif opcion == "eliminar":
            if categoria == "Medicamento":
                print("Eliminar")
                #EliminarManager(Medicamento, request)
            elif categoria == "Animal":
                print("Eliminar")
                #EliminarManager(Animal, request)
            elif categoria == "Enfermedad":
                print("Eliminar")
                #EliminarManager(Enfermedad, request)
            return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso="Se elimino: ")


@app.route('/agregarDosis', methods=['GET','POST'])
def agregarDosis():
    global usuarioAdentro
    opcion = request.form['submit']
    if opcion == "agregar":
        suceso = InsertarDosis(request)
    elif opcion == "modificar":
        print("Modificar")
    elif opcion == "eliminar":
        print("Eliminar")
    return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso=suceso)



@app.route('/agregarPrescripcion', methods=['GET','POST'])
def agregarPrescripcion():
    global usuarioAdentro
    opcion = request.form['submit']
    if opcion == "agregar":
        suceso = InsertarPrescripcion(request)
    elif opcion == "modificar":
        print("Modificar")
    elif opcion == "eliminar":
        print("Eliminar")
    return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuarioAdentro, suceso=suceso)



# @app.route('/register', methods=['GET','POST'])
# def register():
#     if 'fotoSubida' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     nombreCompleto = request.form['nombreCompleto']
#     usuario = request.form['usuario']
#     contrasena = request.form['contrasena']
#     permiso = request.form['permiso']
#     foto = request.files['fotoSubida']
#     if foto.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if foto and allowed_file(foto.filename):
#         filename = secure_filename(foto.filename)
#         foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     InsertarUsuario(usuario, contrasena, nombreCompleto, permiso, foto)
#     return render_template("login.html", suceso="Se agregaron los datos")

# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('template.html', filename=filename)
#
# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# @app.route("/nombre")
# @app.route("/nombre/<name>")  # Toma la url + una variable y la devuelve al html designado.
# def nombre(name=None):
#     return render_template("profile.html", name=name)
#
#
# @app.route("/procesar", methods=['GET','POST'])
# def procesar():
#     return render_template("profile.html", name="Hola")
#
# @app.route("/compras", methods=['GET','POST'])  # Pasando objetos. Una lista de productos.
# def compras():
#     apellidoE = request.form['name']
#     print(apellidoE)
#     return render_template("comprando.html", comida=salude(), persona=persona1, nombreE=apellidoE)
#
#
# @app.route('/_add_numbers')
# def add_numbers():
#     """Add two numbers server side, ridiculous but well..."""
#     a = request.args.get('a', 0, type=int)
#     b = request.args.get('b', 0, type=int)
#     return jsonify(result=a + b)



# Esto lo hace correr. El debug = true permite que se impriman los errores, si se quita igual funciona

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)
