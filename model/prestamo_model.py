from mongodb import MongoDB

class PrestamoModel:
    def __init__(self):
        db = MongoDB()
        self.collection = db.db["prestamos"]

    def listar_prestamos(self):
        return list(self.collection.find({}, {"_id": 0}))

    def crear_prestamo(self, prestamo):
        self.collection.insert_one(prestamo)

    def eliminar_prestamo(self, usuario, libro):
        self.collection.delete_one({"usuario": usuario, "libro": libro})
