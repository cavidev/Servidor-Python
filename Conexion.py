
__author__ = 'Carlos Mario'
import mysql.connector
from mysql.connector import MySQLConnection, Error
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
cursor.close()
conexion_mysql.close()

def listaAnimales():
    global cursor
    cursor.execute("Select * from animales")
    return

#Recorre la consulta hecha, los campos recibidos se transforma en lo que son ejemplo un int, viene aka como un int.
for (Campo1, Campo2, Campo3,Campo4, Campo5) in cursor:
    print("Campo1: ", Campo1, ", Campo2: " + Campo2 + ", Campo3: " + Campo3 + ",Campo4: " + Campo4 + ",Campo5: ",Campo5)

def obtenerUsuarioBD():
    conexion_mysql = mysql.connector.connect(**config_mysql)
    cursor = conexion_mysql.cursor()
    cursor.execute("Select * from usuario")


    listaUsuarios = []
    for (login, contasena, nombre, permiso, foto) in cursor:
        diccionario = {"nombreUsuario": login, "contrasena": contasena,"nombre":nombre, "permiso":permiso,"foto":foto}
        listaUsuarios.append(diccionario)
    cursor.close()
    conexion_mysql.close()
    return listaUsuarios



    return

# Cerramos la variable encargada de las consultas y la conexion
#************************************************
#Esta sirve..¡¡

def insertarUsuarioBD(login, contrasena, nombre, permiso,foto):

    #prepare update query and data
    query = "INSERT INTO usuario(login, contrasena, nombre, permiso,foto)VALUES(%s,%s,%s,%s,%s)"

    args = (login, contrasena, nombre, permiso,foto)

    try:
        conexion_mysql = mysql.connector.connect(**config_mysql)
        cursor = conexion_mysql.cursor()
        cursor.execute(query, args)
        conexion_mysql.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conexion_mysql.close()

