from model.prestamo_model import PrestamoModel
from model.usuario_model import UsuarioModel
from model.libro_model import LibroModel
from datetime import datetime

class PrestamoController:
    def __init__(self):
        self.modelo = PrestamoModel()
        self.usuario_model = UsuarioModel()
        self.libro_model = LibroModel()

    # === LISTADOS ===
    def listar_prestamos(self):
        return self.modelo.listar_prestamos()

    def listar_usuarios(self):
        return self.usuario_model.listar_usuarios()

    def listar_libros_disponibles(self):
        """Retorna libros que estén disponibles y con stock > 0"""
        return [l for l in self.libro_model.listar_libros() if l["estado"] == "Disponible" and l["stock"] > 0]

    # === REGISTRO DE PRÉSTAMO ===
    def registrar_prestamo(self, usuario_nombre, libros_seleccionados, fecha_devolucion):
        """
        Registra un préstamo con múltiples libros y cantidades.
        Disminuye el stock de cada libro y actualiza su estado.
        """
        if not usuario_nombre:
            raise ValueError("Debe seleccionar un usuario.")
        if not libros_seleccionados:
            raise ValueError("Debe agregar al menos un libro.")
        if not fecha_devolucion:
            raise ValueError("Debe seleccionar una fecha de devolución.")

        fecha_actual = datetime.today().strftime("%Y-%m-%d")

        # Validar disponibilidad y actualizar stock
        for item in libros_seleccionados:
            titulo = item["titulo"]
            cantidad = int(item.get("cantidad", 1))

            libro = next((l for l in self.libro_model.listar_libros() if l["titulo"] == titulo), None)
            if not libro:
                raise ValueError(f"El libro '{titulo}' no existe.")
            if libro["stock"] < cantidad:
                raise ValueError(f"No hay suficiente stock para '{titulo}'. Disponible: {libro['stock']}")

            # Actualizar stock y estado
            nuevo_stock = libro["stock"] - cantidad
            nuevo_estado = "Prestado" if nuevo_stock == 0 else "Disponible"

            self.libro_model.actualizar_libro(
                libro["titulo"],
                libro["autor"],
                {**libro, "stock": nuevo_stock, "estado": nuevo_estado}
            )

        # Crear registro de préstamo
        prestamo = {
            "usuario": usuario_nombre,
            "libros": libros_seleccionados,
            "fecha_prestamo": fecha_actual,
            "fecha_devolucion": fecha_devolucion
        }

        self.modelo.crear_prestamo(prestamo)

    # === ELIMINACIÓN DE PRÉSTAMO (DEVOLUCIÓN) ===
    def eliminar_prestamo(self, usuario_nombre):
        """
        Marca el préstamo como devuelto:
        - Elimina el préstamo de la base de datos
        - Restaura el stock de los libros
        """
        prestamos = self.modelo.listar_prestamos()
        prestamo = next((p for p in prestamos if p["usuario"] == usuario_nombre), None)
        if not prestamo:
            raise ValueError("No se encontró préstamo para este usuario.")

        for l in prestamo.get("libros", []):
            titulo = l["titulo"]
            cantidad = int(l.get("cantidad", 1))

            libro = next((b for b in self.libro_model.listar_libros() if b["titulo"] == titulo), None)
            if not libro:
                continue

            nuevo_stock = libro["stock"] + cantidad
            nuevo_estado = "Disponible"

            self.libro_model.actualizar_libro(
                libro["titulo"],
                libro["autor"],
                {**libro, "stock": nuevo_stock, "estado": nuevo_estado}
            )

        self.modelo.eliminar_prestamo(usuario_nombre)
