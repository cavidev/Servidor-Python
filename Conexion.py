
__author__ = 'Carlos Mario'
import mysql.connector
from DTO import *

# Variable con la configuracion de la conexion
config_mysql = {
    'user': 'root', #Nombre de usuario
    'password': '2016',#La contraseña de la base de datos
    'host': 'localhost',#127.0.0.1 #El host que va a utilizar.
    'database': 'veterinariaEYC',#Nombre de la base de datos, en este caso es un ejemplo de ella misma
}

# conectamos al servidor MySql
conexion_mysql = mysql.connector.connect(**config_mysql)

#Cursor de conexion.
cursor = conexion_mysql.cursor()

#Ejecutando una consulta de la base DB
#cursor.execute("select * from city")

def listar(nombreTabla):
    conexion_mysql = mysql.connector.connect(**config_mysql)
    cursor = conexion_mysql.cursor()
    cursor.execute("Select * from "+ nombreTabla().getClase())
    listaElementos = []
    for (nombre, descripcion, foto) in cursor:
        nuevo = nombreTabla()
        nuevo.setNombre(nombre)
        nuevo.setDescripcion(descripcion)
        nuevo.setFoto(foto)
        listaElementos.append(nuevo)
    cursor.close()
    conexion_mysql.close()
    return listaElementos

def listarDosis():
    conexion_mysql = mysql.connector.connect(**config_mysql)
    cursor = conexion_mysql.cursor()
    cursor.execute("Select * from Dosis")
    listaElementos = []
    for (id,animal,medicamento,enfermedad,peso,dosis) in cursor:
        nuevo = Dosis()
        nuevo.setID(id)
        nuevo.setAnimal(animal)
        nuevo.setMedicamento(medicamento)
        nuevo.setEnfermedad(enfermedad)
        nuevo.setPeso(peso)
        nuevo.setDosis(dosis)
        listaElementos.append(nuevo)
    cursor.close()
    conexion_mysql.close()
    return listaElementos

def listarPrescripciones():
    conexion_mysql = mysql.connector.connect(**config_mysql)
    cursor = conexion_mysql.cursor()
    cursor.execute("Select * from Prescripcion")
    listaElementos = []
    for (id,usuario, animal, enfermedad, peso, idDosis) in cursor:
        nuevo = Prescripcion()
        nuevo.setID(id)
        nuevo.setUsuario(usuario)
        nuevo.setAnimal(animal)
        nuevo.setEnfermedad(enfermedad)
        nuevo.setPeso(peso)
        nuevo.setDosis(idDosis)
        listaElementos.append(nuevo)
    cursor.close()
    conexion_mysql.close()
    return listaElementos

#Recorre la consulta hecha, los campos recibidos se transforma en lo que son ejemplo un int, viene aka como un int.
for (Campo1, Campo2, Campo3,Campo4, Campo5) in cursor:
    print("Campo1: ", Campo1, ", Campo2: " + Campo2 + ", Campo3: " + Campo3 + ",Campo4: " + Campo4 + ",Campo5: ",Campo5)

def obtenerUsuarioBD():
    conexion_mysql = mysql.connector.connect(**config_mysql)
    cursor = conexion_mysql.cursor()
    cursor.execute("Select * from usuario")
    listaUsuarios = []
    for (login, contrasena, nombre, permiso, foto) in cursor:
        nuevo = Usuario()
        nuevo.setLogin(login)
        nuevo.setPassword(contrasena)
        nuevo.setNombre(nombre)
        nuevo.setPermiso(permiso)
        nuevo.setFoto(foto)
        listaUsuarios.append(nuevo)
    cursor.close()
    conexion_mysql.close()
    return listaUsuarios



# Cerramos la variable encargada de las consultas y la conexion
cursor.close()
conexion_mysql.close()
