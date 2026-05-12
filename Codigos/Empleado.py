from Persona import Persona

class Empleado(Persona):
    def __init__(self, **kwargs):
        super().__init__(
            kwargs.get('idUnico'),
            kwargs.get('nombre',''),
            kwargs.get('direccion',''),
            kwargs.get('telefono',''),
            kwargs.get('correo',''),
            kwargs.get('fechacontrato',''),
            kwargs.get('salario',0)
        )
        self.__departamento_id = kwargs.get('departamento_id')
        self.__username = kwargs.get('username','')
        self.__password_hash = kwargs.get('password_hash','')

    def get_departamento_id(self):
        return self.__departamento_id
    def set_departamento_id(self, dep_id):
        self.__departamento_id = dep_id
    def get_username(self):
        return self.__username
    def get_password_hash(self):
        return self.__password_hash

    def mostrarRol(self):
        return f"Empleado: {self.get_nombre()}"