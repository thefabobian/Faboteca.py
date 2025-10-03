import tkinter as tk
from view.libro_view import LibroView
from controller.libro_controller import LibroController

def main():
    root = tk.Tk()
    controlador = LibroController()
    LibroView(root, controlador)
    root.mainloop()

if __name__ == "__main__":
    main()
