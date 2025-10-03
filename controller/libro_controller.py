from model.libro_model import LibroModel

class LibroController:
    def __init__(self):
        self.model = LibroModel()

    def listar_libros(self):
        return self.model.leer_libros()

    def crear_libro(self, libro):
        self.model.crear_libro(libro)

    def actualizar_libro(self, index, libro_actualizado):
        self.model.actualizar_libro(index, libro_actualizado)

    def eliminar_libro(self, index):
        self.model.eliminar_libro(index)