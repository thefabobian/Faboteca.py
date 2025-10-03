import os
from pymongo import MongoClient
from dotenv import load_dotenv   # <- CORRECTO

# Cargar variables de entorno desde .env
load_dotenv()

class MongoDB:
    def __init__(self):
        uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("MONGODB_DB")

        if not uri or not db_name:
            raise ValueError("❌ Falta configurar MONGODB_URI o MONGODB_DB en el archivo .env")

        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)  
        self.db = self.client[db_name]

        # Verificar conexión
        try:
            self.client.admin.command("ping")
            print("✅ Conectado a MongoDB Atlas")
        except Exception as e:
            print("❌ No se pudo conectar a MongoDB Atlas:", e)

    def get_collection(self, name):
        return self.db[name]
