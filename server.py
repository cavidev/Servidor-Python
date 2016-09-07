from flask import Flask  # Esta siempre va en proyectos de flask
from flask import request  # Permite hacer los metodos HTTP (GET,POST)
from flask import render_template
from flask import jsonify
from manager import *

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
        return render_template("index.html", error="Datos incorrectos")
    elif(usuario.getPermiso() == "admin"):
        return render_template("usuarioAdmin/usuarioAdmi.html", usuario=usuario)
    elif(usuario.getPermiso() == "normal"):
        return render_template("usuarioAdmi.html", usuario=usuario)



@app.route("/nombre")
@app.route("/nombre/<name>")  # Toma la url + una variable y la devuelve al html designado.
def nombre(name=None):
    return render_template("profile.html", name=name)

#
# @app.route("/procesar", methods=['GET','POST'])
# def procesar():
#     apellidoE = request.form['name']
#     return render_template("comprando.html", comida=salude(), persona=persona1, nombreE=apellidoE)
#
# @app.route("/compras", methods=['GET','POST'])  # Pasando objetos. Una lista de productos.
# def compras():
#     apellidoE = request.form['name']
#     print(apellidoE)
#     return render_template("comprando.html", comida=salude(), persona=persona1, nombreE=apellidoE)


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
    app.run(debug=True)
