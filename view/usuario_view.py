import tkinter as tk
from tkinter import ttk, messagebox

class UsuarioView:
    def __init__(self, master, controlador):
        self.master = master
        self.controlador = controlador
        self.master.title("Gestión de Usuarios")

        # Formulario
        tk.Label(master, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(master)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Cédula:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_cedula = tk.Entry(master)
        self.entry_cedula.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="Correo:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_correo = tk.Entry(master)
        self.entry_correo.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        tk.Button(master, text="Agregar", command=self.agregar_usuario).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(master, text="Actualizar", command=self.actualizar_usuario).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(master, text="Eliminar", command=self.eliminar_usuario).grid(row=3, column=2, padx=5, pady=5)

        # Tabla
        self.tree = ttk.Treeview(master, columns=("Nombre", "Cédula", "Correo"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cédula", text="Cédula")
        self.tree.heading("Correo", text="Correo")
        self.tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.refrescar()

    def agregar_usuario(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "cedula": self.entry_cedula.get(),
            "correo": self.entry_correo.get()
        }
        self.controlador.crear_usuario(datos)
        self.refrescar()

    def actualizar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario")
            return
        index = self.tree.index(seleccionado[0])
        datos = {
            "nombre": self.entry_nombre.get(),
            "cedula": self.entry_cedula.get(),
            "correo": self.entry_correo.get()
        }
        self.controlador.actualizar_usuario(index, datos)
        self.refrescar()

    def eliminar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario")
            return
        index = self.tree.index(seleccionado[0])
        self.controlador.eliminar_usuario(index)
        self.refrescar()

    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for usuario in self.controlador.listar_usuarios():
            self.tree.insert("", "end", values=(usuario["nombre"], usuario["cedula"], usuario["correo"]))
