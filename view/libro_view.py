import tkinter as tk
from tkinter import ttk, messagebox

class LibroView:
    def __init__(self, master, controlador, ventana_principal=None):
        self.master = master
        self.controlador = controlador
        self.ventana_principal = ventana_principal
        self.master.title("Gestión de Libros")

        # Variables para los Entry
        self.var_titulo = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_genero = tk.StringVar()
        self.var_estado = tk.StringVar(value="Disponible")

        # Formulario
        tk.Label(master, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_titulo = tk.Entry(master, textvariable=self.var_titulo)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_autor = tk.Entry(master, textvariable=self.var_autor)
        self.entry_autor.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Género:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_genero = tk.Entry(master, textvariable=self.var_genero)
        self.entry_genero.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Estado:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.combo_estado = ttk.Combobox(master, textvariable=self.var_estado, values=["Disponible", "Prestado"], state="readonly")
        self.combo_estado.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botones
        tk.Button(master, text="Agregar", command=self.agregar_libro).grid(row=4, column=0, padx=5, pady=8)
        tk.Button(master, text="Actualizar", command=self.actualizar_libro).grid(row=4, column=1, padx=5, pady=8)
        tk.Button(master, text="Eliminar", command=self.eliminar_libro).grid(row=4, column=2, padx=5, pady=8)

        # Tabla
        self.tree = ttk.Treeview(master, columns=("Título", "Autor", "Género", "Estado"), show="headings", height=8)
        self.tree.heading("Título", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Estado", text="Estado")
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Bind para seleccionar fila
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Botón para volver al menú principal
        tk.Button(master, text="Volver al Menú Principal", command=self.volver_menu).grid(row=6, column=0, columnspan=3, pady=10)  
        
        # Inicializar vista
        self.refrescar()

        # Scrollbars
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=5, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

    def volver_menu(self):
        if self.ventana_principal:
            self.master.destroy()
            self.ventana_principal.deiconify()
        else:
            self.master.quit()

    # CRUD
    def agregar_libro(self):
        titulo = self.var_titulo.get()
        autor = self.var_autor.get()
        genero = self.var_genero.get()
        estado = self.var_estado.get()

        if not titulo.strip() or not autor.strip() or not genero.strip():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        datos = {"titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
        try:
            self.controlador.crear_libro(datos)
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_libro(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un libro para actualizar")
            return

        values = self.tree.item(sel[0])["values"]
        titulo_original, autor_original = values[0], values[1]

        datos = {
            "titulo": self.var_titulo.get(),
            "autor": self.var_autor.get(),
            "genero": self.var_genero.get(),
            "estado": self.var_estado.get()
        }

        self.controlador.actualizar_libro(titulo_original, autor_original, datos)
        self.refrescar()

    def eliminar_libro(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar")
            return

        values = self.tree.item(sel[0])["values"]
        titulo, autor = values[0], values[1]

        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar '{titulo}' de {autor}?")
        if confirm:
            self.controlador.eliminar_libro(titulo, autor)
            self.refrescar()
    
    def refrescar(self):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        libros = self.controlador.listar_libros()
        for libro in libros:
            self.tree.insert("", "end", values=(libro["titulo"], libro["autor"], libro["genero"], libro["estado"]))

        self.limpiar_formulario()
    
    def limpiar_formulario(self):
        self.var_titulo.set("")
        self.var_autor.set("")
        self.var_genero.set("")
        self.var_estado.set("Disponible")

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0])["values"]
        if values:
            self.var_titulo.set(values[0])
            self.var_autor.set(values[1])
            self.var_genero.set(values[2])
            self.var_estado.set(values[3])
