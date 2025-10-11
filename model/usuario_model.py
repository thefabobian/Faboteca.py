from mongodb import MongoDB
import re

class UsuarioModel:
    def __init__(self):
        db = MongoDB()
        self.collection = db.get_collection("usuarios")

    # --- Listar todos los usuarios ---
    def listar_usuarios(self):
        return list(self.collection.find({}, {"_id": 0}))

    # --- Crear un usuario nuevo ---
    def crear_usuario(self, usuario):
        usuario["cedula"] = str(usuario.get("cedula", "")).strip()
        usuario["nombre"] = usuario.get("nombre", "").strip().upper()
        usuario["correo"] = usuario.get("correo", "").strip()

        # Validaciones de negocio
        if not usuario["nombre"]:
            raise ValueError("El nombre no puede estar vacío.")
        if not usuario["cedula"].isdigit():
            raise ValueError("La cédula debe contener solo números.")
        if not self._correo_valido(usuario["correo"]):
            raise ValueError("El correo no tiene un formato válido.")

        # Validar duplicados
        if self.collection.find_one({"cedula": usuario["cedula"]}):
            raise ValueError("Ya existe un usuario con esta cédula.")
        if self.collection.find_one({"correo": usuario["correo"]}):
            raise ValueError("Ya existe un usuario con este correo.")

        self.collection.insert_one(usuario)

    # --- Actualizar usuario existente ---
    def actualizar_usuario(self, cedula_original, usuario_actualizado):
        # normalizar
        cedula_original = str(cedula_original).strip()
        nuevo_cedula = str(usuario_actualizado.get("cedula", "")).strip()
        nuevo_nombre = usuario_actualizado.get("nombre", "").strip().upper()
        nuevo_correo = usuario_actualizado.get("correo", "").strip()

        usuario_actualizado["cedula"] = nuevo_cedula
        usuario_actualizado["nombre"] = nuevo_nombre
        usuario_actualizado["correo"] = nuevo_correo

        # validaciones básicas
        if not nuevo_nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not nuevo_cedula.isdigit():
            raise ValueError("La cédula debe contener solo números.")
        if not self._correo_valido(nuevo_correo):
            raise ValueError("El correo no tiene un formato válido.")

        # Si la cédula cambió: validar que la nueva cédula no exista en otro documento
        if nuevo_cedula != cedula_original:
            if self.collection.find_one({"cedula": nuevo_cedula}):
                raise ValueError("Ya existe otro usuario con esa cédula.")

        # Para el correo: buscar si existe un documento con ese correo
        # Si existe, permitirlo sólo si pertenece al mismo usuario (misma cedula_original)
        existing = self.collection.find_one({"correo": nuevo_correo})
        if existing and existing.get("cedula") != cedula_original:
            raise ValueError("Ya existe otro usuario con ese correo.")

        # Finalmente, actualizar
        result = self.collection.update_one(
            {"cedula": cedula_original},
            {"$set": usuario_actualizado}
        )
        if result.matched_count == 0:
            raise ValueError("Usuario no encontrado para actualizar.")
        
    # --- Eliminar usuario ---
    def eliminar_usuario(self, cedula):
        cedula = str(cedula)
        result = self.collection.delete_one({"cedula": cedula})
        if result.deleted_count == 0:
            raise ValueError("No se encontró el usuario para eliminar.")

    # --- Validar formato de correo ---
    def _correo_valido(self, correo):
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.match(patron, correo)
