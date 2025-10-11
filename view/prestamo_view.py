import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class PrestamoView:
    def __init__(self, master, controlador, ventana_principal=None):
        self.master = master
        self.controlador = controlador
        self.ventana_principal = ventana_principal
        self.master.title("📚 Gestión de Préstamos - Faboteca")
        self.master.configure(bg="#f5f6f7")
        self.master.geometry("950x650")

        # Variables
        self.var_usuario = tk.StringVar()
        self.var_libro = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_cantidad = tk.IntVar(value=1)

        # Lista temporal
        self.libros_seleccionados = []

        # === FRAME USUARIO ===
        frame_usuario = ttk.LabelFrame(master, text="👤 Usuario", padding=10)
        frame_usuario.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_usuario, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_usuario = ttk.Combobox(frame_usuario, textvariable=self.var_usuario, state="readonly", width=40)
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # === FRAME LIBRO + TABLA TEMPORAL ===
        frame_contenido = ttk.Frame(master)
        frame_contenido.pack(fill="both", expand=True, padx=10, pady=5)

        # Subframe izquierdo (selección libro)
        frame_libro = ttk.LabelFrame(frame_contenido, text="📘 Selección de Libros", padding=10)
        frame_libro.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(frame_libro, text="Libro:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_libro = ttk.Combobox(frame_libro, textvariable=self.var_libro, state="readonly", width=40)
        self.combo_libro.grid(row=0, column=1, padx=5, pady=5)
        self.combo_libro.bind("<<ComboboxSelected>>", self.actualizar_autor)

        ttk.Label(frame_libro, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame_libro, textvariable=self.var_autor, state="readonly", width=42).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_libro, text="Cantidad:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame_libro, textvariable=self.var_cantidad, width=10).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame_libro, text="➕ Agregar libro", command=self.agregar_libro).grid(row=3, column=1, pady=10, sticky="e")

        # Subframe derecho (tabla temporal)
        frame_temp = ttk.LabelFrame(frame_contenido, text="🧾 Libros del préstamo actual", padding=10)
        frame_temp.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        columnas_temp = ("Título", "Autor", "Cantidad")
        self.tree_temp = ttk.Treeview(frame_temp, columns=columnas_temp, show="headings", height=7)
        for col in columnas_temp:
            self.tree_temp.heading(col, text=col)
            self.tree_temp.column(col, width=160)
        self.tree_temp.pack(fill="both", expand=True, pady=5)

        ttk.Button(frame_temp, text="🗑️ Quitar libro", command=self.quitar_libro).pack(pady=5)

        frame_contenido.columnconfigure(0, weight=1)
        frame_contenido.columnconfigure(1, weight=1)

        # === FRAME FECHAS ===
        frame_accion = ttk.LabelFrame(master, text="🕒 Registro de préstamo", padding=10)
        frame_accion.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_accion, text="Fecha préstamo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(frame_accion, text=datetime.today().strftime("%Y-%m-%d")).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_accion, text="Fecha de devolución:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.fecha_devolucion = DateEntry(frame_accion, date_pattern="yyyy-mm-dd", mindate=datetime.today(), width=12)
        self.fecha_devolucion.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame_accion, text="💾 Registrar préstamo", command=self.registrar_prestamo).grid(row=2, column=0, columnspan=2, pady=8)

        # === FRAME HISTORIAL ===
        frame_tabla = ttk.LabelFrame(master, text="📚 Historial de préstamos", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("Usuario", "Libros", "Fecha préstamo", "Fecha devolución")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(fill="both", expand=True)

        ttk.Button(frame_tabla, text="📉 Eliminar préstamo (devolución)", command=self.eliminar_prestamo).pack(pady=8)

        ttk.Button(frame_tabla, text="📊 Ver estadísticas", command=self.abrir_estadisticas).pack(pady=5)
        ttk.Button(master, text="⬅️ Volver al menú principal", command=self.volver_menu).pack(pady=10)

        self.refrescar()

    # ---------- FUNCIONES ----------
    def volver_menu(self):
        if self.ventana_principal:
            self.master.destroy()
            self.ventana_principal.deiconify()
        else:
            self.master.quit()

    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.tree_temp.get_children():
            self.tree_temp.delete(row)
        self.libros_seleccionados.clear()

        usuarios = self.controlador.listar_usuarios()
        self.combo_usuario["values"] = [u["nombre"] for u in usuarios]

        libros = self.controlador.listar_libros_disponibles()
        self.combo_libro["values"] = [l["titulo"] for l in libros]

        prestamos = self.controlador.listar_prestamos()
        for p in prestamos:
            libros_str = ", ".join([f"{l.get('titulo', 'Desconocido')} ({l.get('cantidad', 1)}x)" for l in p.get("libros", [])])
            self.tree.insert("", "end", values=(
                p["usuario"], libros_str, p["fecha_prestamo"], p["fecha_devolucion"]
            ))

        self.var_libro.set("")
        self.var_autor.set("")
        self.var_cantidad.set(1)

    def actualizar_autor(self, event=None):
        titulo = self.var_libro.get()
        libros = self.controlador.listar_libros_disponibles()
        libro = next((l for l in libros if l["titulo"] == titulo), None)
        self.var_autor.set(libro["autor"] if libro else "")

    def agregar_libro(self):
        titulo = self.var_libro.get()
        autor = self.var_autor.get()
        try:
            cantidad = int(self.var_cantidad.get())
        except Exception:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        if not titulo:
            messagebox.showerror("Error", "Debe seleccionar un libro.")
            return
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor o igual a 1.")
            return

        # buscar stock actual en la base (no confiar sólo en la UI)
        libro_db = next((l for l in self.controlador.listar_libros_disponibles() if l["titulo"] == titulo), None)
        if not libro_db:
            messagebox.showerror("Error", f"El libro '{titulo}' no está disponible actualmente.")
            return
        stock_disponible = int(libro_db.get("stock", 0))

        # cantidad ya seleccionada en la lista temporal para ese título
        cantidad_actual_seleccionada = sum(item["cantidad"] for item in self.libros_seleccionados if item["titulo"] == titulo)

        if cantidad_actual_seleccionada + cantidad > stock_disponible:
            messagebox.showerror("Error", f"No hay suficiente stock para '{titulo}'. Disponible: {stock_disponible - cantidad_actual_seleccionada}")
            return

        # Si ya existe en la lista temporal, lo consolidamos (aumentamos cantidad)
        for idx, item in enumerate(self.libros_seleccionados):
            if item["titulo"] == titulo:
                item["cantidad"] += cantidad
                # actualizar la fila correspondiente en tree_temp (los hijos se mantienen en el mismo orden que la lista)
                children = self.tree_temp.get_children()
                if idx < len(children):
                    self.tree_temp.item(children[idx], values=(item["titulo"], item["autor"], item["cantidad"]))
                else:
                    # fallback: buscar por título
                    for node in children:
                        vals = self.tree_temp.item(node)["values"]
                        if vals and vals[0] == titulo:
                            self.tree_temp.item(node, values=(item["titulo"], item["autor"], item["cantidad"]))
                            break
                break
        else:
            # no existía: agregar nuevo
            nuevo = {"titulo": titulo, "autor": autor, "cantidad": cantidad}
            self.libros_seleccionados.append(nuevo)
            self.tree_temp.insert("", "end", values=(titulo, autor, cantidad))

        # limpiar selección en UI
        self.var_libro.set("")
        self.var_autor.set("")
        self.var_cantidad.set(1)

    def quitar_libro(self):
        sel = self.tree_temp.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un libro para quitar.")
            return

        # obtenemos el índice de la fila seleccionada en la treeview y lo sincronizamos con la lista temporal
        index = self.tree_temp.index(sel[0])
        try:
            # eliminar de la lista temporal
            self.libros_seleccionados.pop(index)
        except IndexError:
            # Fallback: intentar eliminar por título si el índice falla
            vals = self.tree_temp.item(sel[0])["values"]
            if vals:
                titulo = vals[0]
                # quitar la primera ocurrencia con ese título
                for i, it in enumerate(self.libros_seleccionados):
                    if it["titulo"] == titulo:
                        self.libros_seleccionados.pop(i)
                        break

        # quitar fila de la treeview
        self.tree_temp.delete(sel[0])


    def registrar_prestamo(self):
        usuario = self.var_usuario.get()
        fecha_dev = self.fecha_devolucion.get_date().strftime("%Y-%m-%d")

        if not usuario:
            messagebox.showerror("Error", "Debe seleccionar un usuario.")
            return
        if not self.libros_seleccionados:
            messagebox.showerror("Error", "Debe agregar al menos un libro.")
            return

        try:
            self.controlador.registrar_prestamo(usuario, self.libros_seleccionados, fecha_dev)
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def eliminar_prestamo(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un préstamo para eliminar.")
            return

        usuario = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"¿Marcar devolución para el préstamo de {usuario}?"):
            try:
                self.controlador.eliminar_prestamo(usuario)
                messagebox.showinfo("Éxito", "Préstamo eliminado y stock actualizado.")
                self.refrescar()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                
    def abrir_estadisticas(self):
        from view.estadisticas_view import EstadisticasView
        ventana = tk.Toplevel(self.master)
        EstadisticasView(ventana, self.controlador)
