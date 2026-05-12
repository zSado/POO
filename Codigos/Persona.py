class Persona:
    def __init__(self,idUnico,nombre,direccion,telefono,correo,fechacontrato,salario):
        self.__idUnico = idUnico
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__correo = correo
        self.__fechacontrato = fechacontrato
        self.__salario = salario
    
    def set_idUnico(self,idUnico):
        self.__idUnico = idUnico
    
    def get_idUnico(self):
        return self.__idUnico

    def set_nombre(self,nombre):
        self.__nombre = nombre
    
    def get_nombre(self):
        return self.__nombre

    def set_direccion(self,direccion):
        self.__direccion = direccion

    def get_direccion(self):
        return self.__direccion

    def set_telefono(self,telefono):
        self.__telefono = telefono
    
    def get_telefono(self):
        return self.__telefono

    def set_correo(self,correo):
        self.__correo = correo
    
    def get_correo(self):
        return self.__correo

    def set_fechacontrato(self,fechacontrato):
        self.__fechacontrato = fechacontrato
    
    def get_fechacontrato(self):
        return self.__fechacontrato

    def set_salario(self,salario):
        self.__salario = salario
    
    def get_salario(self):
        return self.__salario