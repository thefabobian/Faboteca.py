import tkinter as tk
from tkinter import ttk, messagebox

class LibroView:
    def __init__(self, master, controlador):
        self.master = master
        self.controlador = controlador
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

        # Inicializar vista
        self.refrescar()

        # Scrollbars
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=5, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

    # VALIDACIONES título, autor, género y evitar duplicados
    def validar_datos(self, titulo, autor, genero, estado, index=None):
        if not titulo.strip():
            messagebox.showerror("Error", "El título no puede estar vacío")
            return False
        if not autor.strip():
            messagebox.showerror("Error", "El autor no puede estar vacío")
            return False
        if not genero.strip():
            messagebox.showerror("Error", "El género no puede estar vacío")
            return False

        # Evitar duplicados (título + autor)
        libros = self.controlador.listar_libros()
        for i, l in enumerate(libros):
            if l["titulo"] == titulo and l["autor"] == autor:
                if index is None or index != i:
                    messagebox.showerror("Error", f"El libro '{titulo}' de {autor} ya está registrado")
                    return False

        return True

    # CRUD
    def agregar_libro(self):
        titulo = self.var_titulo.get()
        autor = self.var_autor.get()
        genero = self.var_genero.get()
        estado = self.var_estado.get()

        if not self.validar_datos(titulo, autor, genero, estado):
            return

        datos = {"titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
        self.controlador.crear_libro(datos)
        self.refrescar()

    def actualizar_libro(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un libro para actualizar")
            return

        index = self.tree.index(sel[0])

        titulo = self.var_titulo.get()
        autor = self.var_autor.get()
        genero = self.var_genero.get()
        estado = self.var_estado.get()

        if not self.validar_datos(titulo, autor, genero, estado, index = index):
            return

        datos = {"titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
        self.controlador.actualizar_libro(index, datos)
        self.refrescar()

    def eliminar_libro(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar")
            return

        index = self.tree.index(sel[0])
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el libro seleccionado?")
        if confirm:
            self.controlador.eliminar_libro(index)
            self.refrescar()
    
    def refrescar(self):
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Cargar datos
        libros = self.controlador.listar_libros()
        for libro in libros:
            self.tree.insert("", "end", values=(libro["titulo"], libro["autor"], libro["genero"], libro["estado"]))

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
        self.var_titulo.set("")
        self.var_autor.set("")
        self.var_genero.set("")
        self.var_estado.set("Disponible")

    # Manejo selección (cuando el usuario hace click)  
    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        index = self.tree.index(sel[0])
        libros = self.controlador.listar_libros()
        if index < len(libros):
            l = libros[index]
            # llenar campos con el seleccionado
            self.var_titulo.set(l.get("titulo", ""))
            self.var_autor.set(l.get("autor", ""))
            self.var_genero.set(l.get("genero", ""))
            self.var_estado.set(l.get("estado", ""))