class Proyecto:
    def __init__(self, id=None, nombre="", descripcion="", fechainicio=""):
        self.__id = id
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fechainicio = fechainicio

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, n):
        self.__nombre = n

    def get_descripcion(self):
        return self.__descripcion

    def set_descripcion(self, d):
        self.__descripcion = d

    def get_fechainicio(self):
        return self.__fechainicio

    def set_fechainicio(self, f):
        self.__fechainicio = f