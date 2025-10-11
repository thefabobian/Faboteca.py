from model.libro_model import LibroModel

class LibroController:
    def __init__(self):
        self.model = LibroModel()

    # --- Listar libros ---
    def listar_libros(self):
        try:
            return self.model.listar_libros()
        except Exception as e:
            raise ValueError(f"Error al listar libros: {e}")

    # --- Crear libro ---
    def crear_libro(self, libro):
        try:
            # Normalización de datos antes de enviar al modelo
            libro["titulo"] = libro.get("titulo", "").strip()
            libro["autor"] = libro.get("autor", "").strip()
            libro["genero"] = libro.get("genero", "").strip()
            libro["estado"] = libro.get("estado", "Disponible").strip()
            libro["stock"] = int(libro.get("stock", 1))

            # Validación de negocio antes del modelo
            if not libro["titulo"] or not libro["autor"] or not libro["genero"]:
                raise ValueError("Todos los campos son obligatorios.")
            if libro["stock"] < 0:
                raise ValueError("El stock no puede ser negativo.")
            if libro["estado"] not in ["Disponible", "Prestado"]:
                raise ValueError("El estado debe ser 'Disponible' o 'Prestado'.")

            # Enviar al modelo
            self.model.crear_libro(libro)

        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al crear el libro: {e}")

    # --- Actualizar libro ---
    def actualizar_libro(self, titulo_original, autor_original, libro_actualizado):
        try:
            # Limpieza y validación previa
            libro_actualizado["titulo"] = libro_actualizado.get("titulo", "").strip()
            libro_actualizado["autor"] = libro_actualizado.get("autor", "").strip()
            libro_actualizado["genero"] = libro_actualizado.get("genero", "").strip()
            libro_actualizado["estado"] = libro_actualizado.get("estado", "Disponible").strip()
            libro_actualizado["stock"] = int(libro_actualizado.get("stock", 1))

            if not libro_actualizado["titulo"] or not libro_actualizado["autor"] or not libro_actualizado["genero"]:
                raise ValueError("Título, autor y género son obligatorios.")
            if libro_actualizado["stock"] < 0:
                raise ValueError("El stock no puede ser negativo.")

            # Ajustar estado automáticamente
            if libro_actualizado["stock"] == 0:
                libro_actualizado["estado"] = "Prestado"
            else:
                libro_actualizado["estado"] = "Disponible"

            self.model.actualizar_libro(titulo_original, autor_original, libro_actualizado)

        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al actualizar el libro: {e}")

    # --- Eliminar libro ---
    def eliminar_libro(self, titulo, autor):
        try:
            self.model.eliminar_libro(titulo, autor)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al eliminar el libro: {e}")
