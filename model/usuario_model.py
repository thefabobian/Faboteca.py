from mongodb import MongoDB

class UsuarioModel:
    def __init__(self):
        db = MongoDB()
        self.collection = db.get_collection("usuarios")

    def listar_usuarios(self):
        # devolvemos lista de usuarios sin el _id interno de Mongo
        return list(self.collection.find({}, {"_id": 0}))

    def crear_usuario(self, usuario):
        self.collection.insert_one(usuario)

    def actualizar_usuario(self, cedula, usuario_actualizado):
        # buscamos por cédula porque es nuestro identificador único
        self.collection.update_one({"cedula": cedula}, {"$set": usuario_actualizado})

    def eliminar_usuario(self, cedula):
        self.collection.delete_one({"cedula": cedula})
