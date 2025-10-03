import json
import os

class UsuarioModel:
    def __init__(self, archivo="data/usuarios.json"):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump([], f)

    def leer_usuarios(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def guardar_usuarios(self, usuarios):
        with open(self.archivo, "w") as f:
            json.dump(usuarios, f, indent=4)

    def crear_usuario(self, usuario):
        usuarios = self.leer_usuarios()
        usuarios.append(usuario)
        self.guardar_usuarios(usuarios)

    def actualizar_usuario(self, index, usuario_actualizado):
        usuarios = self.leer_usuarios()
        usuarios[index] = usuario_actualizado
        self.guardar_usuarios(usuarios)

    def eliminar_usuario(self, index):
        usuarios = self.leer_usuarios()
        usuarios.pop(index)
        self.guardar_usuarios(usuarios)
