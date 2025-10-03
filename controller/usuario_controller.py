from model.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()

    def listar_usuarios(self):
        return self.model.listar_usuarios()

    def crear_usuario(self, usuario):
        self.model.crear_usuario(usuario)

    def actualizar_usuario(self, cedula, usuario_actualizado):
        self.model.actualizar_usuario(cedula, usuario_actualizado)

    def eliminar_usuario(self, cedula):
        self.model.eliminar_usuario(cedula)
