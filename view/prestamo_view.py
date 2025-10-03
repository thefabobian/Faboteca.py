import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class PrestamoView:
    def __init__(self, master, controlador, ventana_principal=None):
        self.master = master
        self.controlador = controlador
        self.ventana_principal = ventana_principal
        self.master.title("Gestión de Préstamos")

        # Variables
        self.var_usuario = tk.StringVar()
        self.var_libro = tk.StringVar()
        self.var_fecha = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))

        # Formulario
        tk.Label(master, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_usuario = ttk.Combobox(master, textvariable=self.var_usuario, state="readonly")
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Libro:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_libro = ttk.Combobox(master, textvariable=self.var_libro, state="readonly")
        self.combo_libro.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(master, text="Fecha:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_fecha = tk.Entry(master, textvariable=self.var_fecha, state="readonly")
        self.entry_fecha.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        tk.Button(master, text="Registrar", command=self.agregar_prestamo).grid(row=3, column=0, padx=5, pady=8)
        tk.Button(master, text="Eliminar", command=self.eliminar_prestamo).grid(row=3, column=1, padx=5, pady=8)

        # Tabla
        self.tree = ttk.Treeview(master, columns=("Usuario", "Libro", "Fecha"), show="headings", height=8)
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Libro", text="Libro")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # botón para volver al menú principal
        tk.Button(master, text="Volver al Menú Principal", command=self.volver_menu).grid(row=5, column=0, columnspan=3, pady=10)
        
        self.refrescar()

    def volver_menu(self):
        if self.ventana_principal:
            self.master.destroy()
            self.ventana_principal.deiconify()
        else:
            self.master.quit()

    def refrescar(self):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Poblar tabla con préstamos
        prestamos = self.controlador.listar_prestamos()
        for p in prestamos:
            self.tree.insert("", "end", values=(p["usuario"], p["libro"], p["fecha"]))

        # Poblar comboboxes
        usuarios = self.controlador.usuario_model.listar_usuarios()
        self.combo_usuario["values"] = [u["nombre"] for u in usuarios]

        libros = self.controlador.libro_model.listar_libros()
        self.combo_libro["values"] = [l["titulo"] for l in libros if l["estado"] == "Disponible"]

        self.var_usuario.set("")
        self.var_libro.set("")
        self.var_fecha.set(datetime.today().strftime("%Y-%m-%d"))

    def agregar_prestamo(self):
        usuario = self.var_usuario.get()
        libro = self.var_libro.get()
        fecha = self.var_fecha.get()

        if not usuario or not libro:
            messagebox.showerror("Error", "Debe seleccionar usuario y libro")
            return

        prestamo = {"usuario": usuario, "libro": libro, "fecha": fecha}
        if self.controlador.crear_prestamo(prestamo):
            self.refrescar()
        else:
            messagebox.showerror("Error", "El libro ya está prestado")

    def eliminar_prestamo(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un préstamo")
            return

        values = self.tree.item(sel[0])["values"]
        usuario, libro = values[0], values[1]

        if messagebox.askyesno("Confirmar", f"¿Desea eliminar el préstamo de '{libro}' por {usuario}?"):
            self.controlador.eliminar_prestamo(usuario, libro)
            self.refrescar()
