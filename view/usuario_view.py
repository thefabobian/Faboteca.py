import tkinter as tk
from tkinter import ttk, messagebox
import re

class UsuarioView:
    def __init__(self, master, controlador, ventana_principal=None):
        self.master = master
        self.controlador = controlador
        self.ventana_principal = ventana_principal
        self.master.title("Gestión de Usuarios")

        # Variables
        self.var_nombre = tk.StringVar()
        self.var_cedula = tk.StringVar()
        self.var_correo = tk.StringVar()

        # ----------- FORMULARIO -----------
        tk.Label(master, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_nombre).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Cédula:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_cedula).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Correo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_correo).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # ----------- BOTONES -----------
        tk.Button(master, text="Agregar", command=self.agregar_usuario).grid(row=3, column=0, padx=5, pady=8)
        tk.Button(master, text="Actualizar", command=self.actualizar_usuario).grid(row=3, column=1, padx=5, pady=8)
        tk.Button(master, text="Eliminar", command=self.eliminar_usuario).grid(row=3, column=2, padx=5, pady=8)

        # ----------- TABLA -----------
        self.tree = ttk.Treeview(master, columns=("Nombre", "Cédula", "Correo"), show="headings", height=8)
        for col in ("Nombre", "Cédula", "Correo"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=4, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Vincular selección de fila
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Botón para volver
        tk.Button(master, text="Volver al Menú Principal", command=self.volver_menu).grid(row=5, column=0, columnspan=3, pady=10)

        # Inicializar vista
        self.refrescar()

    # ----------- NAVEGACIÓN -----------
    def volver_menu(self):
        if self.ventana_principal:
            self.master.destroy()
            self.ventana_principal.deiconify()
        else:
            self.master.quit()

    # ----------- VALIDACIÓN -----------
    def validar_datos(self, nombre, cedula, correo):
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return False

        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula solo puede contener números.")
            return False

        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, correo.strip()):
            messagebox.showerror("Error", "El correo no es válido.")
            return False

        return True

    # ----------- CRUD -----------
    def agregar_usuario(self):
        nombre = self.var_nombre.get()
        cedula = self.var_cedula.get()
        correo = self.var_correo.get()

        if not self.validar_datos(nombre, cedula, correo):
            return

        datos = {"nombre": nombre, "cedula": cedula, "correo": correo}
        try:
            self.controlador.crear_usuario(datos)
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario para actualizar.")
            return

        cedula_original = self.tree.item(seleccionado[0])["values"][1]
        nombre = self.var_nombre.get()
        cedula = self.var_cedula.get()
        correo = self.var_correo.get()

        if not self.validar_datos(nombre, cedula, correo):
            return

        datos = {"nombre": nombre, "cedula": cedula, "correo": correo}
        try:
            self.controlador.actualizar_usuario(cedula_original, datos)
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario para eliminar.")
            return

        cedula = self.tree.item(seleccionado[0])["values"][1]
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este usuario?"):
            try:
                self.controlador.eliminar_usuario(cedula)
                self.refrescar()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # ----------- REFRESCAR DATOS -----------
    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = self.controlador.listar_usuarios()
        for u in usuarios:
            self.tree.insert("", "end", values=(u["nombre"], u["cedula"], u["correo"]))
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.var_nombre.set("")
        self.var_cedula.set("")
        self.var_correo.set("")

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        if values:
            self.var_nombre.set(values[0])
            self.var_cedula.set(values[1])
            self.var_correo.set(values[2])
