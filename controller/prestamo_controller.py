from model.prestamo_model import PrestamoModel
from model.usuario_model import UsuarioModel
from model.libro_model import LibroModel

class PrestamoController:
    def __init__(self):
        self.modelo = PrestamoModel()
        self.usuario_model = UsuarioModel()
        self.libro_model = LibroModel()

    def listar_prestamos(self):
        return self.modelo.listar_prestamos()

    def crear_prestamo(self, prestamo):
        # Validar si el libro está disponible
        libros = self.libro_model.listar_libros()
        for l in libros:
            if l["titulo"] == prestamo["libro"] and l["estado"] == "Disponible":
                # cambiar estado a "Prestado"
                self.libro_model.actualizar_libro(l["titulo"], l["autor"], {**l, "estado": "Prestado"})
                self.modelo.crear_prestamo(prestamo)
                return True
        return False

    def eliminar_prestamo(self, usuario, libro):
        # Al eliminar préstamo, cambiar libro a "Disponible"
        libros = self.libro_model.listar_libros()
        for l in libros:
            if l["titulo"] == libro:
                self.libro_model.actualizar_libro(l["titulo"], l["autor"], {**l, "estado": "Disponible"})
                break

        self.modelo.eliminar_prestamo(usuario, libro)
