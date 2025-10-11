import tkinter as tk
from tkinter import ttk, messagebox

class LibroView:
    def __init__(self, master, controlador, ventana_principal=None):
        self.master = master
        self.controlador = controlador
        self.ventana_principal = ventana_principal
        self.master.title("Gestión de Libros")

        # Variables
        self.var_titulo = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_genero = tk.StringVar()
        self.var_estado = tk.StringVar(value="Disponible")
        self.var_stock = tk.IntVar(value=1)

        # ----------- FORMULARIO -----------
        tk.Label(master, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_titulo).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_autor).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Género:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_genero).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Estado:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Combobox(master, textvariable=self.var_estado,
                     values=["Disponible", "Prestado"], state="readonly").grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Stock:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.var_stock).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # ----------- BOTONES -----------
        tk.Button(master, text="Agregar", command=self.agregar_libro).grid(row=5, column=0, padx=5, pady=8)
        tk.Button(master, text="Actualizar", command=self.actualizar_libro).grid(row=5, column=1, padx=5, pady=8)
        tk.Button(master, text="Eliminar", command=self.eliminar_libro).grid(row=5, column=2, padx=5, pady=8)

        # ----------- TABLA -----------
        self.tree = ttk.Treeview(master, columns=("Título", "Autor", "Género", "Estado", "Stock"),
                                 show="headings", height=8)
        for col in ("Título", "Autor", "Género", "Estado", "Stock"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Scrollbar
        vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        vsb.grid(row=6, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Selección
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Botón volver
        tk.Button(master, text="Volver al Menú Principal",
                  command=self.volver_menu).grid(row=7, column=0, columnspan=3, pady=10)

        # Cargar datos
        self.refrescar()

    # ----------- NAVEGACIÓN -----------
    def volver_menu(self):
        if self.ventana_principal:
            self.master.destroy()
            self.ventana_principal.deiconify()
        else:
            self.master.quit()

    # ----------- CRUD -----------
    def agregar_libro(self):
        titulo = self.var_titulo.get()
        autor = self.var_autor.get()
        genero = self.var_genero.get()
        estado = self.var_estado.get()
        stock = self.var_stock.get()

        if not titulo.strip() or not autor.strip() or not genero.strip():
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if stock < 0:
            messagebox.showerror("Error", "El stock no puede ser negativo.")
            return

        datos = {"titulo": titulo, "autor": autor, "genero": genero, "estado": estado, "stock": stock}
        try:
            self.controlador.crear_libro(datos)
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_libro(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un libro para actualizar.")
            return

        values = self.tree.item(sel[0])["values"]
        titulo_original, autor_original = values[0], values[1]

        datos = {
            "titulo": self.var_titulo.get(),
            "autor": self.var_autor.get(),
            "genero": self.var_genero.get(),
            "estado": self.var_estado.get(),
            "stock": self.var_stock.get()
        }

        try:
            self.controlador.actualizar_libro(titulo_original, autor_original, datos)
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_libro(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar.")
            return

        values = self.tree.item(sel[0])["values"]
        titulo, autor = values[0], values[1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar '{titulo}' de {autor}?"):
            try:
                self.controlador.eliminar_libro(titulo, autor)
                self.refrescar()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # ----------- REFRESCAR DATOS -----------
    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        libros = self.controlador.listar_libros()
        for libro in libros:
            self.tree.insert("", "end", values=(
                libro.get("titulo", ""),
                libro.get("autor", ""),
                libro.get("genero", ""),
                libro.get("estado", ""),
                libro.get("stock", 0)
            ))

        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.var_titulo.set("")
        self.var_autor.set("")
        self.var_genero.set("")
        self.var_estado.set("Disponible")
        self.var_stock.set(1)

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
            self.var_stock.set(values[4])
 