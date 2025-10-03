import tkinter as tk
from controller.usuario_controller import UsuarioController
from controller.libro_controller import LibroController
from controller.prestamo_controller import PrestamoController
from view.usuario_view import UsuarioView
from view.libro_view import LibroView
from view.prestamo_view import PrestamoView

class MenuView:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Biblioteca - Menú Principal")
        self.master.geometry("400x250")

        tk.Label(master, text="Sistema de Biblioteca", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(master, text="Gestión de Usuarios", width=25, command=self.abrir_usuarios).pack(pady=5)
        tk.Button(master, text="Gestión de Libros", width=25, command=self.abrir_libros).pack(pady=5)
        tk.Button(master, text="Gestión de Préstamos", width=25, command=self.abrir_prestamos).pack(pady=5)

        tk.Button(master, text="Salir", width=25, command=master.quit).pack(pady=20)

    def abrir_usuarios(self):
        self.master.withdraw()  # ocultar menú
        ventana = tk.Toplevel()
        UsuarioView(ventana, UsuarioController(), self.master)

    def abrir_libros(self):
        self.master.withdraw()
        ventana = tk.Toplevel()
        LibroView(ventana, LibroController(), self.master)

    def abrir_prestamos(self):
        self.master.withdraw()
        ventana = tk.Toplevel()
        PrestamoView(ventana, PrestamoController(), self.master)
