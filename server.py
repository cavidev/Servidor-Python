import io
import os
import base64
from flask import Flask,request,render_template,jsonify,redirect, url_for # Esta siempre va en proyectos de flask
from flask import flash
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
        return redirect(request.url)
    nombreCompleto = request.form['nombreCompleto']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    permiso = request.form['permiso']
    foto = request.files['fotoSubida'].read()
    foto1 = request.files['fotoSubida']

    if foto1.filename == '':
         flash('No selected file')
         return redirect(request.url)
    if foto1 and allowed_file(foto1.filename):
         filename = secure_filename(foto1.filename)
         foto1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         #InsertarUsuarioManager(usuario, contrasena, nombreCompleto, permiso, foto)
    bytes = bytearray(foto)
    #imagen64 = base64.encodebytes(foto)
    imagen64 = base64.b64encode(foto)
    print(imagen64)

    imagen = base64.decodebytes(imagen64)
    return render_template("profile.html", suceso=imagen64)



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


# Esto lo hace correr. El debug = true permite que se impriman los errores, si se quita igual funciona
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)
