from Empleado import Empleado

class Gerente(Empleado):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__managed_departamento_id = kwargs.get('managed_departamento_id')

    def evaluarEmpleado(self, empleado_id, comentario):
        print(f"Evaluando empleado {empleado_id}: {comentario}")

    def mostrarRol(self):
        return f"Gerente: {self.get_nombre()} (Gestiona depto {self.__managed_departamento_id})"