from Persona import Persona

class Administrador(Persona):
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
        self.__username = kwargs.get('username','')
        self.__password_hash = kwargs.get('password_hash','')

    def generarInforme(self, tipo='pdf'):
        print(f"Generando informe {tipo.upper()} (simulado)")

    def gestionarEmpleados(self):
        print("CRUD de empleados")
    def gestionarDepartamento(self):
        print("CRUD de departamentos")
    def gestionarProyectos(self):
        print("CRUD de proyectos")

    def mostrarRol(self):
        return f"Administrador: {self.get_nombre()}"