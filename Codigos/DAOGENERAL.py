import json
from Conexion import Conexion

class DAOGENERAL:
    #Departamento
    @staticmethod
    def guardar_departamento(conexion, id_dep, nombre, tipo):
        try:
            conn, cursor = conexion.conectar()
            if id_dep is None:
                sql = "INSERT INTO departamento (nombre, tipoDepartamento) VALUES (%s, %s)"
                cursor.execute(sql, (nombre, tipo))
                nuevo_id = cursor.lastrowid
                print("Departamento creado correctamente.")
            else:
                sql = "UPDATE departamento SET nombre=%s, tipoDepartamento=%s WHERE id=%s"
                cursor.execute(sql, (nombre, tipo, id_dep))
                nuevo_id = id_dep
                print("Departamento actualizado correctamente.")
            conn.commit()
            conexion.desconectar()
            return nuevo_id
        except Exception as e:
            print(f"Error guardando departamento: {e}")
            return None

    @staticmethod
    def listar_departamentos(conexion):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("SELECT id, nombre, tipoDepartamento FROM departamento")
            rows = cursor.fetchall()
            conexion.desconectar()
            return rows
        except Exception as e:
            print(f"Error listando departamentos: {e}")
            return []

    @staticmethod
    def eliminar_departamento(conexion, id_dep):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("DELETE FROM departamento WHERE id=%s", (id_dep,))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error eliminando departamento: {e}")
            return False

    #Proyecto
    @staticmethod
    def guardar_proyecto(conexion, id_proy, nombre, descripcion, fechainicio):
        try:
            conn, cursor = conexion.conectar()
            if id_proy is None:
                sql = "INSERT INTO proyecto (nombre, descripcion, fechaInicio) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nombre, descripcion, fechainicio))
                nuevo_id = cursor.lastrowid
                print("Proyecto creado correctamente.")
            else:
                sql = "UPDATE proyecto SET nombre=%s, descripcion=%s, fechaInicio=%s WHERE id=%s"
                cursor.execute(sql, (nombre, descripcion, fechainicio, id_proy))
                nuevo_id = id_proy
                print("Proyecto actualizado correctamente.")
            conn.commit()
            conexion.desconectar()
            return nuevo_id
        except Exception as e:
            print(f"Error guardando proyecto: {e}")
            return None

    @staticmethod
    def listar_proyectos(conexion):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("SELECT id, nombre, descripcion, fechaInicio FROM proyecto")
            rows = cursor.fetchall()
            conexion.desconectar()
            return rows
        except Exception as e:
            print(f"Error listando proyectos: {e}")
            return []

    @staticmethod
    def eliminar_proyecto(conexion, id_proy):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("DELETE FROM proyecto WHERE id=%s", (id_proy,))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error eliminando proyecto: {e}")
            return False

    @staticmethod
    def asignar_empleado_proyecto(conexion, empleado_id, proyecto_id):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("INSERT INTO asignacion_proyecto (empleado_id, proyecto_id) VALUES (%s, %s)",
                           (empleado_id, proyecto_id))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error asignando empleado: {e}")
            return False

    @staticmethod
    def desasignar_empleado_proyecto(conexion, empleado_id, proyecto_id):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("DELETE FROM asignacion_proyecto WHERE empleado_id=%s AND proyecto_id=%s",
                           (empleado_id, proyecto_id))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error desasignando empleado: {e}")
            return False

    #Registro de Tiempo
    @staticmethod
    def guardar_registro_tiempo(conexion, id_reg, empleado_id, proyecto_id, fecha, horas, tareas):
        try:
            conn, cursor = conexion.conectar()
            if id_reg is None:
                sql = """INSERT INTO registro_tiempo 
                         (empleado_id, proyecto_id, fecha, horasTrabajadas, tareasRealizadas)
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (empleado_id, proyecto_id, fecha, horas, tareas))
                nuevo_id = cursor.lastrowid
                print("Registro de tiempo guardado.")
            else:
                sql = """UPDATE registro_tiempo 
                         SET empleado_id=%s, proyecto_id=%s, fecha=%s, horasTrabajadas=%s, tareasRealizadas=%s
                         WHERE id=%s"""
                cursor.execute(sql, (empleado_id, proyecto_id, fecha, horas, tareas, id_reg))
                nuevo_id = id_reg
                print("Registro de tiempo actualizado.")
            conn.commit()
            conexion.desconectar()
            return nuevo_id
        except Exception as e:
            print(f"Error guardando registro: {e}")
            return None

    @staticmethod
    def listar_registros_por_empleado(conexion, empleado_id):
        try:
            conn, cursor = conexion.conectar()
            sql = """SELECT rt.*, p.nombre as proyecto_nombre 
                     FROM registro_tiempo rt
                     JOIN proyecto p ON rt.proyecto_id = p.id
                     WHERE rt.empleado_id = %s
                     ORDER BY rt.fecha DESC"""
            cursor.execute(sql, (empleado_id,))
            rows = cursor.fetchall()
            conexion.desconectar()
            return rows
        except Exception as e:
            print(f"Error listando registros: {e}")
            return []

    @staticmethod
    def eliminar_registro_tiempo(conexion, id_reg):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("DELETE FROM registro_tiempo WHERE id=%s", (id_reg,))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error eliminando registro: {e}")
            return False

    #Persona
    @staticmethod
    def crear_persona(conexion, datos):
        """datos debe contener: idUnico, nombre, direccion, telefono, correo, fechaInicioContrato,
           salario, username, password_hash, rol, departamento_id, managed_departamento_id"""
        try:
            conn, cursor = conexion.conectar()
            sql = """INSERT INTO persona 
                     (idUnico, nombre, direccion, telefono, correo, fechaInicioContrato, salario,
                      username, password_hash, rol, departamento_id, managed_departamento_id)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                datos['idUnico'], datos['nombre'], datos['direccion'], datos['telefono'],
                datos['correo'], datos['fechacontrato'], datos['salario'],
                datos['username'], datos['password_hash'], datos['rol'],
                datos['departamento_id'], datos['managed_departamento_id']
            ))
            conn.commit()
            conexion.desconectar()
            print("Persona creada exitosamente.")
            return True
        except Exception as e:
            print(f"Error creando persona: {e}")
            return False

    @staticmethod
    def actualizar_persona(conexion, idUnico, datos):
        try:
            conn, cursor = conexion.conectar()
            sql = """UPDATE persona SET
                     nombre=%s, direccion=%s, telefono=%s, correo=%s, fechaInicioContrato=%s, salario=%s,
                     username=%s, password_hash=%s, rol=%s, departamento_id=%s, managed_departamento_id=%s
                     WHERE idUnico=%s"""
            cursor.execute(sql, (
                datos['nombre'], datos['direccion'], datos['telefono'], datos['correo'],
                datos['fechacontrato'], datos['salario'], datos['username'], datos['password_hash'],
                datos['rol'], datos['departamento_id'], datos['managed_departamento_id'],
                idUnico
            ))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error actualizando persona: {e}")
            return False

    @staticmethod
    def eliminar_persona(conexion, idUnico):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("DELETE FROM persona WHERE idUnico=%s", (idUnico,))
            conn.commit()
            conexion.desconectar()
            return True
        except Exception as e:
            print(f"Error eliminando persona: {e}")
            return False

    @staticmethod
    def listar_personas(conexion):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("SELECT * FROM persona")
            rows = cursor.fetchall()
            conexion.desconectar()
            return rows
        except Exception as e:
            print(f"Error listando personas: {e}")
            return []

    @staticmethod
    def obtener_persona_por_username(conexion, username):
        try:
            conn, cursor = conexion.conectar()
            cursor.execute("SELECT * FROM persona WHERE username=%s", (username,))
            row = cursor.fetchone()
            conexion.desconectar()
            return row
        except Exception as e:
            print(f"Error obteniendo persona: {e}")
            return None