from pymongo import MongoClient
import os
import certifi  

# Configuración con seguridad SSL
MONGO_URI = os.getenv("MONGO_URI", 
    f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@"
    f"{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DB', 'eventos')}"
    "?retryWrites=true&w=majority&tls=true&tlsCAFile={}".format(certifi.where()))

client = MongoClient(
    MONGO_URI,
    connectTimeoutMS=5000,
    socketTimeoutMS=30000,
    serverSelectionTimeoutMS=5000
)

db = client.get_database(os.getenv("MONGO_DB", "eventos"))
events_collection = db.get_collection(os.getenv("MONGO_COLLECTION", "eventos_scrap"))
#crudos_collection = db.get_collection("eventos_crudos")