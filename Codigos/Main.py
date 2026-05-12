import hashlib
from Conexion import Conexion
from Persona import Persona
from Empleado import Empleado
from Gerente import Gerente
from Administrador import Administrador
from Departamento import Departamento
from Proyecto import Proyecto
from RegistroTiempo import RegistroTiempo
from DAOGENERAL import DAOGENERAL

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def autenticar(conexion, username, password):
    user_data = DAOGENERAL.obtener_persona_por_username(conexion, username)
    if user_data and user_data['password_hash'] == hash_password(password):
        return user_data
    return None

def cargar_usuario(data):
    rol = data['rol']
    kwargs = {
        'idUnico': data['idUnico'],
        'nombre': data['nombre'],
        'direccion': data['direccion'],
        'telefono': data['telefono'],
        'correo': data['correo'],
        'fechacontrato': str(data['fechaInicioContrato']),
        'salario': data['salario'],
        'username': data['username'],
        'password_hash': data['password_hash'],
        'departamento_id': data['departamento_id'],
        'managed_departamento_id': data['managed_departamento_id']
    }
    if rol == 'Administrador':
        return Administrador(**kwargs)
    elif rol == 'Gerente':
        return Gerente(**kwargs)
    else:
        return Empleado(**kwargs)

def menu_empleado(usuario, conexion):
    while True:
        print("\n=== EMPLEADO ===")
        print("1. Registrar horas")
        print("2. Ver mis horas")
        print("3. Salir")
        op = input("Opción: ")
        if op == '1':
            pid = int(input("ID proyecto: "))
            fecha = input("Fecha (YYYY-MM-DD): ")
            horas = float(input("Horas: "))
            tarea = input("Tarea realizada: ")
            DAOGENERAL.guardar_registro_tiempo(
                conexion, None, usuario.get_idUnico(), pid, fecha, horas, tarea
            )
        elif op == '2':
            registros = DAOGENERAL.listar_registros_por_empleado(conexion, usuario.get_idUnico())
            if not registros:
                print("No hay registros.")
            else:
                for r in registros:
                    print(f"{r['fecha']} | Proyecto: {r['proyecto_nombre']} | Horas: {r['horasTrabajadas']} | Tarea: {r['tareasRealizadas']}")
        elif op == '3':
            break

def menu_gerente(usuario, conexion):
    while True:
        print("\n=== GERENTE ===")
        print("1. Evaluar empleado")
        print("2. Listar empleados")
        print("3. Registrar horas (propio)")
        print("4. Salir")
        op = input("Opción: ")
        if op == '1':
            eid = input("ID del empleado: ")
            com = input("Comentario de evaluación: ")
            usuario.evaluarEmpleado(eid, com)
        elif op == '2':
            empleados = DAOGENERAL.listar_personas(conexion)
            for emp in empleados:
                print(f"{emp['idUnico']} - {emp['nombre']} ({emp['rol']})")
        elif op == '3':
            pid = int(input("ID proyecto: "))
            fecha = input("Fecha (YYYY-MM-DD): ")
            horas = float(input("Horas: "))
            tarea = input("Tarea realizada: ")
            DAOGENERAL.guardar_registro_tiempo(
                conexion, None, usuario.get_idUnico(), pid, fecha, horas, tarea
            )
        elif op == '4':
            break

def menu_admin(usuario, conexion):
    while True:
        print("\n=== ADMINISTRADOR ===")
        print("1. Crear empleado")
        print("2. Listar empleados")
        print("3. Crear departamento")
        print("4. Listar departamentos")
        print("5. Crear proyecto")
        print("6. Listar proyectos")
        print("7. Asignar empleado a proyecto")
        print("8. Generar informe (simulado)")
        print("9. Salir")
        op = input("Opción: ")

        if op == '1':
            print("\n--- CREAR NUEVO EMPLEADO ---")
            idUnico = input("ID único: ")
            nombre = input("Nombre completo: ")
            direccion = input("Dirección: ")
            telefono = input("Teléfono: ")
            correo = input("Correo electrónico: ")
            fechacontrato = input("Fecha de contrato (YYYY-MM-DD): ")
            salario = float(input("Salario: "))
            username = input("Nombre de usuario: ")
            pwd = input("Contraseña: ")
            rol = input("Rol (Empleado/Gerente/Administrador): ")
            depto_id = input("ID del departamento (opcional, dejar vacío si no): ") or None
            managed_depto = input("ID departamento que gerencia (solo para Gerente): ") or None

            datos = {
                'idUnico': idUnico,
                'nombre': nombre,
                'direccion': direccion,
                'telefono': telefono,
                'correo': correo,
                'fechacontrato': fechacontrato,
                'salario': salario,
                'username': username,
                'password_hash': hash_password(pwd),
                'rol': rol,
                'departamento_id': depto_id,
                'managed_departamento_id': managed_depto
            }
            DAOGENERAL.crear_persona(conexion, datos)

        elif op == '2':
            personas = DAOGENERAL.listar_personas(conexion)
            if not personas:
                print("No hay empleados registrados.")
            else:
                for p in personas:
                    print(f"{p['idUnico']} - {p['nombre']} ({p['rol']})")

        elif op == '3':
            nombre = input("Nombre del departamento: ")
            tipo = input("Tipo del departamento: ")
            nuevo_id = DAOGENERAL.guardar_departamento(conexion, None, nombre, tipo)
            if nuevo_id:
                print(f"Departamento creado con ID {nuevo_id}")

        elif op == '4':
            deptos = DAOGENERAL.listar_departamentos(conexion)
            if not deptos:
                print("No hay departamentos.")
            else:
                for d in deptos:
                    print(f"{d['id']} - {d['nombre']} ({d['tipoDepartamento']})")

        elif op == '5':
            nombre = input("Nombre del proyecto: ")
            desc = input("Descripción: ")
            fecha = input("Fecha de inicio (YYYY-MM-DD): ")
            nuevo_id = DAOGENERAL.guardar_proyecto(conexion, None, nombre, desc, fecha)
            if nuevo_id:
                print(f"Proyecto creado con ID {nuevo_id}")

        elif op == '6':
            proys = DAOGENERAL.listar_proyectos(conexion)
            if not proys:
                print("No hay proyectos.")
            else:
                for p in proys:
                    print(f"{p['id']} - {p['nombre']} - Inicio: {p['fechaInicio']}")

        elif op == '7':
            eid = input("ID del empleado: ")
            pid = input("ID del proyecto: ")
            ok = DAOGENERAL.asignar_empleado_proyecto(conexion, eid, pid)
            if ok:
                print("Asignación realizada.")
            else:
                print("Error en la asignación (verifique IDs o duplicado).")

        elif op == '8':
            usuario.generarInforme()

        elif op == '9':
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    db = Conexion()
    print("=== Sistema Gestión de Empleados ===")
    user = input("Usuario: ")
    pwd = input("Contraseña: ")

    user_data = autenticar(db, user, pwd)
    if not user_data:
        print("Acceso denegado")
        exit()

    usuario = cargar_usuario(user_data)
    print(f"Bienvenido {usuario.get_nombre()} - {usuario.mostrarRol()}")

    if isinstance(usuario, Administrador):
        menu_admin(usuario, db)
    elif isinstance(usuario, Gerente):
        menu_gerente(usuario, db)
    else:
        menu_empleado(usuario, db)