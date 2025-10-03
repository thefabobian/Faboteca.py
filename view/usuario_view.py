# vistas/usuario_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class UsuarioView:
    def __init__(self, master, controlador):
        self.master = master
        self.controlador = controlador
        self.master.title("Gestión de Usuarios")

        # Variables para los Entry (usar StringVar hace más fiable limpiar y setear)
        self.var_nombre = tk.StringVar()
        self.var_cedula = tk.StringVar()
        self.var_correo = tk.StringVar()

        # Formulario
        tk.Label(master, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(master, textvariable=self.var_nombre)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Cédula:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_cedula = tk.Entry(master, textvariable=self.var_cedula)
        self.entry_cedula.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Correo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_correo = tk.Entry(master, textvariable=self.var_correo)
        self.entry_correo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Botones
        tk.Button(master, text="Agregar", command=self.agregar_usuario).grid(row=3, column=0, padx=5, pady=8)
        tk.Button(master, text="Actualizar", command=self.actualizar_usuario).grid(row=3, column=1, padx=5, pady=8)
        tk.Button(master, text="Eliminar", command=self.eliminar_usuario).grid(row=3, column=2, padx=5, pady=8)

        # Tabla
        self.tree = ttk.Treeview(master, columns=("Nombre", "Cédula", "Correo"), show="headings", height=8)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cédula", text="Cédula")
        self.tree.heading("Correo", text="Correo")
        self.tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Scrollbars (opcional, recomendado)
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=4, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Bind para seleccionar fila (sólo llena campos cuando el usuario hace selección manual)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Inicializar vista
        self.refrescar()

    # -------------------
    # VALIDACIONES (ejemplo: cédula numérica y correos válidos)
    # -------------------
    def validar_datos(self, nombre, cedula, correo):
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre no puede estar vacío")
            return False
        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula solo puede contener números")
            return False
        dominios_validos = ("@gmail.com", "@hotmail.com", "@outlook.com", "@yahoo.com")
        correo_lower = correo.strip().lower()
        if "@" not in correo_lower or not any(correo_lower.endswith(dom) for dom in dominios_validos):
            messagebox.showerror("Error", "El correo debe ser válido (ej: usuario@gmail.com)")
            return False
        return True

    # -------------------
    # CRUD
    # -------------------
    def agregar_usuario(self):
        nombre = self.var_nombre.get()
        cedula = self.var_cedula.get()
        correo = self.var_correo.get()

        if not self.validar_datos(nombre, cedula, correo):
            return

        datos = {"nombre": nombre, "cedula": cedula, "correo": correo}
        self.controlador.crear_usuario(datos)
        # refrescar() ya limpia el formulario al final
        self.refrescar()

    def actualizar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario para actualizar")
            return
        index = self.tree.index(seleccionado[0])

        nombre = self.var_nombre.get()
        cedula = self.var_cedula.get()
        correo = self.var_correo.get()

        if not self.validar_datos(nombre, cedula, correo):
            return

        datos = {"nombre": nombre, "cedula": cedula, "correo": correo}
        self.controlador.actualizar_usuario(index, datos)
        self.refrescar()

    def eliminar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario para eliminar")
            return
        index = self.tree.index(seleccionado[0])
        # confirmación
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este usuario?"):
            self.controlador.eliminar_usuario(index)
            self.refrescar()

    def refrescar(self):
        # repoblar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = self.controlador.listar_usuarios()
        for usuario in usuarios:
            self.tree.insert("", "end", values=(usuario["nombre"], usuario["cedula"], usuario["correo"]))

        # evitar que la selección automática llene campos: quitar selección si existe
        try:
            current_sel = self.tree.selection()
            if current_sel:
                self.tree.selection_remove(current_sel)
        except Exception:
            pass

        # finalmente limpiar formulario (aquí garantizamos que quede vacío)
        self.limpiar_formulario()

    def limpiar_formulario(self):
        # si usas StringVar -> set('')
        self.var_nombre.set("")
        self.var_cedula.set("")
        self.var_correo.set("")
        # Si no usas StringVar, usar: self.entry_nombre.delete(0, tk.END) etc.

    # -------------------
    # Manejo selección (cuando el usuario hace click)
    # -------------------
    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        usuarios = self.controlador.listar_usuarios()
        if idx < len(usuarios):
            u = usuarios[idx]
            # llenar campos con el seleccionado
            self.var_nombre.set(u.get("nombre", ""))
            self.var_cedula.set(u.get("cedula", ""))
            self.var_correo.set(u.get("correo", ""))
