from Conexion import *
from DTO import *


def obtenerUsuarioManager(nombre,contrasena):
    listaUsuario = obtenerUsuarioBD()
    for usuario in listaUsuario:
        if(usuario["nombreUsuario"]==nombre and usuario["contrasena"]==contrasena):
            usu = Usuario()
            usu.setNombre(usuario["nombre"])
            usu.setLogin(usuario["nombreUsuario"])
            usu.setPassword(usuario["contrasena"])
            usu.setPermiso(usuario["permiso"])
            usu.setFoto(usuario["foto"])
            return usu
    return "error"
