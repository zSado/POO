class RegistroTiempo:
    def __init__(self, id=None, empleado_id=None, proyecto_id=None, fecha="", horasTrabajadas=0, tareasRealizadas=""):
        self.__id = id
        self.__empleado_id = empleado_id
        self.__proyecto_id = proyecto_id
        self.__fecha = fecha
        self.__horasTrabajadas = horasTrabajadas
        self.__tareasRealizadas = tareasRealizadas

    def get_id(self):
        return self.__id

    def get_empleado_id(self):
        return self.__empleado_id

    def set_empleado_id(self, emp_id):
        self.__empleado_id = emp_id

    def get_proyecto_id(self):
        return self.__proyecto_id

    def set_proyecto_id(self, proy_id):
        self.__proyecto_id = proy_id

    def get_fecha(self):
        return self.__fecha

    def set_fecha(self, fecha):
        self.__fecha = fecha

    def get_horas(self):
        return self.__horasTrabajadas

    def set_horas(self, horas):
        self.__horasTrabajadas = horas

    def get_tareasRealizadas(self):
        return self.__tareasRealizadas

    def set_tareasRealizadas(self, tareas):
        self.__tareasRealizadas = tareas