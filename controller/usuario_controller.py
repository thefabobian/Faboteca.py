from model.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self):
        self.model = UsuarioModel()

    def listar_usuarios(self):
        try:
            return self.model.listar_usuarios()
        except Exception as e:
            raise ValueError(f"Error al listar usuarios: {e}")

    def crear_usuario(self, usuario):
        try:
            self.model.crear_usuario(usuario)
        except ValueError as e:
            # Errores de negocio (cedula o correo duplicado)
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al crear el usuario: {e}")

    def actualizar_usuario(self, cedula, usuario_actualizado):
        try:
            self.model.actualizar_usuario(cedula, usuario_actualizado)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al actualizar el usuario: {e}")

    def eliminar_usuario(self, cedula):
        try:
            self.model.eliminar_usuario(cedula)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al eliminar el usuario: {e}")
