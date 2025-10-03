import json
import os

class LibroModel:
    def __init__(self, archivo="data/libros.json"):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump([], f)

    def leer_libros(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def guardar_libros(self, libros):
        with open(self.archivo, "w") as f:
            json.dump(libros, f, indent=4)

    def crear_libro(self, libro):
        libros = self.leer_libros()
        libros.append(libro)
        self.guardar_libros(libros)

    def actualizar_libro(self, index, libro_actualizado):
        libros = self.leer_libros()
        libros[index] = libro_actualizado
        self.guardar_libros(libros)

    def eliminar_libro(self, index):
        libros = self.leer_libros()
        libros.pop(index)
        self.guardar_libros(libros)