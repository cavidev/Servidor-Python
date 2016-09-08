import base64
import io
import os
import base64
from flask import Flask,request,render_template,jsonify,\
    redirect, url_for # Esta siempre va en proyectos de flask
from flask import flash
from flask import send_from_directory
from wand.image import Image
from werkzeug.utils import secure_filename
from manager import *

UPLOAD_FOLDER = 'imagenesUsuario'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif'])


app = Flask(__name__)  # Instancia para llamar a los routers.


@app.route('/')  # Pinta la pagina principal, ´/´ denota la raiz.
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    nombreUsuario = request.form['nombreUsuario']
    contrasena = request.form['contrasena']
    usuario = obtenerUsuarioManager(str(nombreUsuario), str(contrasena))
    if usuario == "error":
        return render_template("index.html", suceso="Datos incorrectos")
    elif(usuario.getPermiso() == "admin"):
        return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuario)
    elif(usuario.getPermiso() == "normal"):
        return render_template("usuarioAdmi.html", usuario=usuario)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/register', methods=['GET','POST'])
def register():
    if 'fotoSubida' not in request.files:
        flash('No file part')
        return redirect(request.url)
    nombreCompleto = request.form['nombreCompleto']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    permiso = request.form['permiso']
    foto = request.files['fotoSubida'].read()
    foto1=request.files['fotoSubida']
    print(foto)
    print(foto1)

    if foto1.filename == '':
         flash('No selected file')
         return redirect(request.url)
    if foto1 and allowed_file(foto1.filename):
         filename = secure_filename(foto1.filename)
         foto1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         #InsertarUsuarioManager(usuario, contrasena, nombreCompleto, permiso, foto)
    bytes = bytearray(foto)
    image = Image.open(io.BytesIO(bytes))
    return render_template("profile.html", suceso=image)

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
#     return render_template("index.html", suceso="Se agregaron los datos")

# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('template.html', filename=filename)
#
# @app.route('/uploads/<filename>')
# def send_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)



@app.route("/nombre")
@app.route("/nombre/<name>")  # Toma la url + una variable y la devuelve al html designado.
def nombre(name=None):
    return render_template("profile.html", name=name)


@app.route("/procesar", methods=['GET','POST'])
def procesar():
    return render_template("profile.html", name="Hola")

@app.route("/compras", methods=['GET','POST'])  # Pasando objetos. Una lista de productos.
def compras():
    apellidoE = request.form['name']
    print(apellidoE)
    return render_template("comprando.html", comida=salude(), persona=persona1, nombreE=apellidoE)


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


# Siempre va la ruta y justo despues la funcion que se dispara cuando en el navegador se pone esa ruta
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text


# Esto lo hace correr. El debug = true permite que se impriman los errores, si se quita igual funciona
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)
