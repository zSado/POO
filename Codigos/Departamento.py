class Departamento:
    def __init__(self, id=None, nombre="", tipoDepartamento=""):
        self.__id = id
        self.__nombre = nombre
        self.__tipoDepartamento = tipoDepartamento

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_tipoDepartamento(self):
        return self.__tipoDepartamento

    def set_tipoDepartamento(self, tipo):
        self.__tipoDepartamento = tipo