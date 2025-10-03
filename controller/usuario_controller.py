from model.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()

    def listar_usuarios(self):
        return self.model.leer_usuarios()

    def crear_usuario(self, usuario):
        self.model.crear_usuario(usuario)

    def actualizar_usuario(self, index, usuario_actualizado):
        self.model.actualizar_usuario(index, usuario_actualizado)

    def eliminar_usuario(self, index):
        self.model.eliminar_usuario(index)