from mongodb import MongoDB

class LibroModel:
    def __init__(self):
        db = MongoDB()
        self.collection = db.db["libros"]

    # --- Listar todos los libros ---
    def listar_libros(self):
        return list(self.collection.find({}, {"_id": 0}))

    # --- Crear libro ---
    def crear_libro(self, libro):
        titulo = libro.get("titulo", "").strip()
        autor = libro.get("autor", "").strip()
        genero = libro.get("genero", "").strip()
        estado = libro.get("estado", "Disponible").strip()
        stock = int(libro.get("stock", 1))

        # --- Validaciones ---
        if not titulo or not autor or not genero:
            raise ValueError("Título, autor y género son obligatorios.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if estado not in ["Disponible", "Prestado"]:
            raise ValueError("El estado debe ser 'Disponible' o 'Prestado'.")

        # Si el stock es 0, debe quedar como Prestado
        if stock == 0:
            estado = "Prestado"
        else:
            estado = "Disponible"

        # --- Evitar duplicados (título + autor) ---
        if self.collection.find_one({"titulo": titulo, "autor": autor}):
            raise ValueError(f"El libro '{titulo}' de {autor} ya existe.")

        nuevo_libro = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado,
            "stock": stock
        }
        self.collection.insert_one(nuevo_libro)

    # --- Actualizar libro ---
    def actualizar_libro(self, titulo_original, autor_original, libro_actualizado):
        titulo = libro_actualizado.get("titulo", "").strip()
        autor = libro_actualizado.get("autor", "").strip()
        genero = libro_actualizado.get("genero", "").strip()
        estado = libro_actualizado.get("estado", "Disponible").strip()
        stock = int(libro_actualizado.get("stock", 1))

        # --- Validaciones ---
        if not titulo or not autor or not genero:
            raise ValueError("Título, autor y género son obligatorios.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if estado not in ["Disponible", "Prestado"]:
            raise ValueError("El estado debe ser 'Disponible' o 'Prestado'.")

        # Ajustar estado automáticamente según stock
        if stock == 0:
            estado = "Prestado"
        else:
            estado = "Disponible"

        # --- Verificar duplicado solo si cambia título o autor ---
        if titulo != titulo_original or autor != autor_original:
            duplicado = self.collection.find_one({"titulo": titulo, "autor": autor})
            if duplicado:
                raise ValueError(f"Ya existe otro libro con el título '{titulo}' y autor '{autor}'.")

        # --- Actualizar ---
        result = self.collection.update_one(
            {"titulo": titulo_original, "autor": autor_original},
            {"$set": {
                "titulo": titulo,
                "autor": autor,
                "genero": genero,
                "estado": estado,
                "stock": stock
            }}
        )
        if result.matched_count == 0:
            raise ValueError("Libro no encontrado para actualizar.")

    # --- Eliminar libro ---
    def eliminar_libro(self, titulo, autor):
        result = self.collection.delete_one({"titulo": titulo, "autor": autor})
        if result.deleted_count == 0:
            raise ValueError("No se encontró el libro para eliminar.")
