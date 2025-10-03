from mongodb import MongoDB

class LibroModel:
    def __init__(self):
        db = MongoDB()
        self.collection = db.db["libros"]

    def listar_libros(self):
        return list(self.collection.find({}, {"_id": 0}))  # sin _id para simplificar

    def crear_libro(self, libro):
        # Verificar duplicado por título + autor
        if self.collection.find_one({"titulo": libro["titulo"], "autor": libro["autor"]}):
            raise ValueError(f"El libro '{libro['titulo']}' de {libro['autor']} ya existe")
        self.collection.insert_one(libro)

    def actualizar_libro(self, titulo_original, autor_original, libro_actualizado):
        self.collection.update_one(
            {"titulo": titulo_original, "autor": autor_original},
            {"$set": libro_actualizado}
        )

    def eliminar_libro(self, titulo, autor):
        self.collection.delete_one({"titulo": titulo, "autor": autor})
