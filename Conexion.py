__author__ = 'Carlos Mario'
import mysql.connector

# Variable con la configuracion de la conexion
config_mysql = {
    'user': 'root', #Nombre de usuario
    'password': '2016',#La contraseña de la base de datos
    'host': 'localhost',#127.0.0.1 #El host que va a utilizar.
    'database': 'world',#Nombre de la base de datos, en este caso es un ejemplo de ella misma
}

# conectamos al servidor MySql
conexion_mysql = mysql.connector.connect(**config_mysql)

#Cursor de conexion.
cursor = conexion_mysql.cursor()

#Ejecutando una consulta de la base DB
cursor.execute("select * from city")

#Recorre la consulta hecha, los campos recibidos se transforma en lo que son ejemplo un int, viene aka como un int.
for (Campo1, Campo2, Campo3,Campo4, Campo5) in cursor:
    print("Campo1: ", Campo1, ", Campo2: " + Campo2 + ", Campo3: " + Campo3 + ",Campo4: " + Campo4 + ",Campo5: ",Campo5)


# Cerramos la variable encargada de las consultas y la conexion
cursor.close()
conexion_mysql.close()
