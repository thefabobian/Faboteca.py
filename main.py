import tkinter as tk
from view.usuario_view import UsuarioView
from controller.usuario_controller import UsuarioController

def main():
    root = tk.Tk()
    controlador = UsuarioController()
    UsuarioView(root, controlador)
    root.mainloop()

if __name__ == "__main__":
    main()
