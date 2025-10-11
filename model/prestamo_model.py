from mongodb import MongoDB

class PrestamoModel:
    def __init__(self):
        db = MongoDB()
        self.collection = db.db["prestamos"]

    def listar_prestamos(self):
        """Lista todos los préstamos registrados"""
        return list(self.collection.find({}, {"_id": 0}))

    def crear_prestamo(self, prestamo):
        """Crea un nuevo préstamo en la base de datos"""
        usuario = prestamo.get("usuario")
        libros = prestamo.get("libros", [])
        fecha_prestamo = prestamo.get("fecha_prestamo")
        fecha_devolucion = prestamo.get("fecha_devolucion")

        if not usuario or not libros:
            raise ValueError("Debe incluir usuario y al menos un libro.")
        if not fecha_prestamo or not fecha_devolucion:
            raise ValueError("Debe incluir fechas válidas.")

        self.collection.insert_one(prestamo)

    def eliminar_prestamo(self, usuario):
        """Elimina un préstamo existente por usuario"""
        result = self.collection.delete_one({"usuario": usuario})
        if result.deleted_count == 0:
            raise ValueError("No se encontró préstamo para eliminar.")
