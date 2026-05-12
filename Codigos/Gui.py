import tkinter as tk
from tkinter import ttk, messagebox
from Conexion import Conexion
from DAOGENERAL import DAOGENERAL
from Empleado import Empleado
from Gerente import Gerente
from Administrador import Administrador
import hashlib

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Empleados")
        self.root.geometry("600x500")
        self.conexion = Conexion()
        self.usuario_actual = None
        self.mostrar_login()

    # ========== LOGIN ==========
    def mostrar_login(self):
        self.limpiar_ventana()
        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 16)).pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_user = tk.Entry(frame)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_pwd = tk.Entry(frame, show="*")
        self.entry_pwd.grid(row=1, column=1, padx=5, pady=5)

        btn_login = tk.Button(self.root, text="Ingresar", command=self.autenticar)
        btn_login.pack(pady=20)

    def autenticar(self):
        user = self.entry_user.get()
        pwd = self.entry_pwd.get()
        if not user or not pwd:
            messagebox.showerror("Error", "Complete ambos campos")
            return
        user_data = DAOGENERAL.obtener_persona_por_username(self.conexion, user)
        if user_data and user_data['password_hash'] == hash_password(pwd):
            # Cargar objeto usuario según rol
            kwargs = {
                'idUnico': user_data['idUnico'],
                'nombre': user_data['nombre'],
                'direccion': user_data['direccion'],
                'telefono': user_data['telefono'],
                'correo': user_data['correo'],
                'fechacontrato': str(user_data['fechaInicioContrato']),
                'salario': user_data['salario'],
                'username': user_data['username'],
                'password_hash': user_data['password_hash'],
                'departamento_id': user_data['departamento_id'],
                'managed_departamento_id': user_data['managed_departamento_id']
            }
            rol = user_data['rol']
            if rol == 'Administrador':
                self.usuario_actual = Administrador(**kwargs)
            elif rol == 'Gerente':
                self.usuario_actual = Gerente(**kwargs)
            else:
                self.usuario_actual = Empleado(**kwargs)
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # ========== MENÚ PRINCIPAL ==========
    def mostrar_menu_principal(self):
        self.limpiar_ventana()
        tk.Label(self.root, text=f"Bienvenido {self.usuario_actual.get_nombre()}", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=self.usuario_actual.mostrarRol(), font=("Arial", 12)).pack(pady=5)

        if isinstance(self.usuario_actual, Administrador):
            self.menu_admin()
        elif isinstance(self.usuario_actual, Gerente):
            self.menu_gerente()
        else:
            self.menu_empleado()

    # ========== MENÚ EMPLEADO ==========
    def menu_empleado(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Button(frame, text="Registrar Horas", command=self.registrar_horas, width=25).pack(pady=5)
        tk.Button(frame, text="Ver Mis Horas", command=self.ver_mis_horas, width=25).pack(pady=5)
        tk.Button(frame, text="Salir", command=self.root.quit, width=25).pack(pady=5)

    def registrar_horas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Horas")
        ventana.geometry("400x300")

        tk.Label(ventana, text="ID Proyecto:").pack(pady=5)
        entry_pid = tk.Entry(ventana)
        entry_pid.pack()

        tk.Label(ventana, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        entry_fecha = tk.Entry(ventana)
        entry_fecha.pack()

        tk.Label(ventana, text="Horas:").pack(pady=5)
        entry_horas = tk.Entry(ventana)
        entry_horas.pack()

        tk.Label(ventana, text="Tarea Realizada:").pack(pady=5)
        entry_tarea = tk.Entry(ventana)
        entry_tarea.pack()

        def guardar():
            try:
                pid = int(entry_pid.get())
                fecha = entry_fecha.get()
                horas = float(entry_horas.get())
                tarea = entry_tarea.get()
                DAOGENERAL.guardar_registro_tiempo(
                    self.conexion, None, self.usuario_actual.get_idUnico(),
                    pid, fecha, horas, tarea
                )
                messagebox.showinfo("Éxito", "Horas registradas correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    def ver_mis_horas(self):
        registros = DAOGENERAL.listar_registros_por_empleado(self.conexion, self.usuario_actual.get_idUnico())
        if not registros:
            messagebox.showinfo("Info", "No hay registros de horas")
            return
        ventana = tk.Toplevel(self.root)
        ventana.title("Mis Horas")
        ventana.geometry("600x400")
        tree = ttk.Treeview(ventana, columns=("fecha", "proyecto", "horas", "tarea"), show="headings")
        tree.heading("fecha", text="Fecha")
        tree.heading("proyecto", text="Proyecto")
        tree.heading("horas", text="Horas")
        tree.heading("tarea", text="Tarea")
        tree.pack(fill=tk.BOTH, expand=True)
        for r in registros:
            tree.insert("", tk.END, values=(r['fecha'], r['proyecto_nombre'], r['horasTrabajadas'], r['tareasRealizadas']))

    # ========== MENÚ GERENTE ==========
    def menu_gerente(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        tk.Button(frame, text="Evaluar Empleado", command=self.evaluar_empleado, width=25).pack(pady=5)
        tk.Button(frame, text="Listar Empleados", command=self.listar_empleados, width=25).pack(pady=5)
        tk.Button(frame, text="Registrar Horas Propio", command=self.registrar_horas, width=25).pack(pady=5)
        tk.Button(frame, text="Salir", command=self.root.quit, width=25).pack(pady=5)

    def evaluar_empleado(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Evaluar Empleado")
        ventana.geometry("300x200")
        tk.Label(ventana, text="ID Empleado:").pack(pady=5)
        entry_id = tk.Entry(ventana)
        entry_id.pack()
        tk.Label(ventana, text="Comentario:").pack(pady=5)
        entry_com = tk.Entry(ventana)
        entry_com.pack()
        def evaluar():
            eid = entry_id.get()
            com = entry_com.get()
            self.usuario_actual.evaluarEmpleado(eid, com)
            messagebox.showinfo("Info", "Evaluación registrada (simulada)")
            ventana.destroy()
        tk.Button(ventana, text="Evaluar", command=evaluar).pack(pady=20)

    def listar_empleados(self):
        empleados = DAOGENERAL.listar_personas(self.conexion)
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Empleados")
        ventana.geometry("500x400")
        tree = ttk.Treeview(ventana, columns=("id", "nombre", "rol"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("rol", text="Rol")
        tree.pack(fill=tk.BOTH, expand=True)
        for emp in empleados:
            tree.insert("", tk.END, values=(emp['idUnico'], emp['nombre'], emp['rol']))

    # ========== MENÚ ADMINISTRADOR ==========
    def menu_admin(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        tk.Button(frame, text="Crear Empleado", command=self.crear_empleado, width=25).pack(pady=5)
        tk.Button(frame, text="Listar Empleados", command=self.listar_empleados, width=25).pack(pady=5)
        tk.Button(frame, text="Crear Departamento", command=self.crear_departamento, width=25).pack(pady=5)
        tk.Button(frame, text="Listar Departamentos", command=self.listar_departamentos, width=25).pack(pady=5)
        tk.Button(frame, text="Crear Proyecto", command=self.crear_proyecto, width=25).pack(pady=5)
        tk.Button(frame, text="Listar Proyectos", command=self.listar_proyectos, width=25).pack(pady=5)
        tk.Button(frame, text="Asignar Empleado a Proyecto", command=self.asignar_empleado_proyecto, width=25).pack(pady=5)
        tk.Button(frame, text="Generar Informe (simulado)", command=self.generar_informe, width=25).pack(pady=5)
        tk.Button(frame, text="Salir", command=self.root.quit, width=25).pack(pady=5)

    def crear_empleado(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Empleado")
        ventana.geometry("400x600")
        campos = ["ID único", "Nombre", "Dirección", "Teléfono", "Correo", "Fecha contrato (YYYY-MM-DD)",
                  "Salario", "Username", "Contraseña", "Rol (Empleado/Gerente/Administrador)",
                  "ID departamento (opcional)", "ID departamento que gerencia (opcional)"]
        entries = {}
        for i, campo in enumerate(campos):
            tk.Label(ventana, text=campo).pack(pady=2)
            entry = tk.Entry(ventana)
            entry.pack(pady=2)
            entries[campo] = entry

        def guardar():
            try:
                datos = {
                    'idUnico': entries["ID único"].get(),
                    'nombre': entries["Nombre"].get(),
                    'direccion': entries["Dirección"].get(),
                    'telefono': entries["Teléfono"].get(),
                    'correo': entries["Correo"].get(),
                    'fechacontrato': entries["Fecha contrato (YYYY-MM-DD)"].get(),
                    'salario': float(entries["Salario"].get()),
                    'username': entries["Username"].get(),
                    'password_hash': hash_password(entries["Contraseña"].get()),
                    'rol': entries["Rol (Empleado/Gerente/Administrador)"].get(),
                    'departamento_id': entries["ID departamento (opcional)"].get() or None,
                    'managed_departamento_id': entries["ID departamento que gerencia (opcional)"].get() or None
                }
                DAOGENERAL.crear_persona(self.conexion, datos)
                messagebox.showinfo("Éxito", "Empleado creado")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    def crear_departamento(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Departamento")
        ventana.geometry("300x200")
        tk.Label(ventana, text="Nombre:").pack()
        nombre_entry = tk.Entry(ventana)
        nombre_entry.pack()
        tk.Label(ventana, text="Tipo:").pack()
        tipo_entry = tk.Entry(ventana)
        tipo_entry.pack()
        def guardar():
            nombre = nombre_entry.get()
            tipo = tipo_entry.get()
            DAOGENERAL.guardar_departamento(self.conexion, None, nombre, tipo)
            messagebox.showinfo("Éxito", "Departamento creado")
            ventana.destroy()
        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    def listar_departamentos(self):
        deptos = DAOGENERAL.listar_departamentos(self.conexion)
        ventana = tk.Toplevel(self.root)
        ventana.title("Departamentos")
        ventana.geometry("400x300")
        tree = ttk.Treeview(ventana, columns=("id", "nombre", "tipo"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("tipo", text="Tipo")
        tree.pack(fill=tk.BOTH, expand=True)
        for d in deptos:
            tree.insert("", tk.END, values=(d['id'], d['nombre'], d['tipoDepartamento']))

    def crear_proyecto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Proyecto")
        ventana.geometry("300x250")
        tk.Label(ventana, text="Nombre:").pack()
        nombre = tk.Entry(ventana)
        nombre.pack()
        tk.Label(ventana, text="Descripción:").pack()
        desc = tk.Entry(ventana)
        desc.pack()
        tk.Label(ventana, text="Fecha inicio (YYYY-MM-DD):").pack()
        fecha = tk.Entry(ventana)
        fecha.pack()
        def guardar():
            DAOGENERAL.guardar_proyecto(self.conexion, None, nombre.get(), desc.get(), fecha.get())
            messagebox.showinfo("Éxito", "Proyecto creado")
            ventana.destroy()
        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

    def listar_proyectos(self):
        proys = DAOGENERAL.listar_proyectos(self.conexion)
        ventana = tk.Toplevel(self.root)
        ventana.title("Proyectos")
        ventana.geometry("500x300")
        tree = ttk.Treeview(ventana, columns=("id", "nombre", "desc", "fecha"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("desc", text="Descripción")
        tree.heading("fecha", text="Fecha Inicio")
        tree.pack(fill=tk.BOTH, expand=True)
        for p in proys:
            tree.insert("", tk.END, values=(p['id'], p['nombre'], p['descripcion'], p['fechaInicio']))

    def asignar_empleado_proyecto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Asignar Empleado a Proyecto")
        ventana.geometry("300x150")
        tk.Label(ventana, text="ID Empleado:").pack()
        eid = tk.Entry(ventana)
        eid.pack()
        tk.Label(ventana, text="ID Proyecto:").pack()
        pid = tk.Entry(ventana)
        pid.pack()
        def asignar():
            ok = DAOGENERAL.asignar_empleado_proyecto(self.conexion, eid.get(), pid.get())
            if ok:
                messagebox.showinfo("Éxito", "Asignación realizada")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo asignar")
        tk.Button(ventana, text="Asignar", command=asignar).pack(pady=20)

    def generar_informe(self):
        self.usuario_actual.generarInforme()
        messagebox.showinfo("Informe", "Informe generado (simulado)")

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()