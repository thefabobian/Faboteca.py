from model.libro_model import LibroModel

class LibroController:
    def __init__(self):
        self.model = LibroModel()

    def listar_libros(self):
        return self.model.listar_libros()

    def crear_libro(self, libro):
        self.model.crear_libro(libro)

    def actualizar_libro(self, titulo_original, autor_original, libro_actualizado):
        self.model.actualizar_libro(titulo_original, autor_original, libro_actualizado)

    def eliminar_libro(self, titulo, autor):
        self.model.eliminar_libro(titulo, autor)
