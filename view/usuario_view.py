import tkinter as tk
from tkinter import ttk, messagebox
import re

class UsuarioView:
    def __init__(self, master, controlador, ventana_principal=None):
        self.master = master
        self.controlador = controlador
        self.ventana_principal = ventana_principal
        self.master.title("Gestión de Usuarios")

        # Variables para los Entry
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

        # Scrollbars
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=4, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Bind para seleccionar fila
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Botón para volver al menú principal
        tk.Button(master, text="Volver al Menú Principal", command=self.volver_menu).grid(row=5, column=0, columnspan=3, pady=10)
        
        # Inicializar vista
        self.refrescar()

    def volver_menu(self):
        if self.ventana_principal:
            self.master.destroy()
            self.ventana_principal.deiconify()
        else:
            self.master.quit()

    # VALIDACIONES nombre, cédula y correo
    def validar_datos(self, nombre, cedula, correo):
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre no puede estar vacío")
            return False
        
        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula solo puede contener números")
            return False
        
        usuarios = self.controlador.listar_usuarios()
        for u in usuarios:
            if u["cedula"] == cedula and u["correo"] != correo:
                messagebox.showerror("Error", "La cédula ya existe")
                return False
        
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, correo.strip()):
            messagebox.showerror("Error", "El correo no es válido")
            return False
        
        for u in usuarios:
            if u["correo"] == correo and u["cedula"] != cedula:
                messagebox.showerror("Error", "El correo ya existe")
                return False
            
        return True

    # CRUD
    def agregar_usuario(self):
        nombre = self.var_nombre.get()
        cedula = self.var_cedula.get()
        correo = self.var_correo.get()

        if not self.validar_datos(nombre, cedula, correo):
            return

        datos = {"nombre": nombre, "cedula": cedula, "correo": correo}
        self.controlador.crear_usuario(datos)
        self.refrescar()

    def actualizar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario para actualizar")
            return

        cedula_original = self.tree.item(seleccionado[0])["values"][1]

        nombre = self.var_nombre.get()
        cedula = self.var_cedula.get()
        correo = self.var_correo.get()

        if not self.validar_datos(nombre, cedula, correo):
            return

        datos = {"nombre": nombre, "cedula": cedula, "correo": correo}
        self.controlador.actualizar_usuario(cedula_original, datos)
        self.refrescar()

    def eliminar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario para eliminar")
            return
        
        cedula = self.tree.item(seleccionado[0])["values"][1]

        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este usuario?"):
            self.controlador.eliminar_usuario(cedula)
            self.refrescar()

    def refrescar(self):
        # repoblar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = self.controlador.listar_usuarios()
        for usuario in usuarios:
            self.tree.insert("", "end", values=(usuario["nombre"], usuario["cedula"], usuario["correo"]))

        # quitar selección
        try:
            current_sel = self.tree.selection()
            if current_sel:
                self.tree.selection_remove(current_sel)
        except Exception:
            pass 

        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.var_nombre.set("")
        self.var_cedula.set("")
        self.var_correo.set("")

    # Manejo selección (cuando el usuario hace click)  
    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        if values:
            self.var_nombre.set(values[0])
            self.var_cedula.set(values[1])
            self.var_correo.set(values[2])
