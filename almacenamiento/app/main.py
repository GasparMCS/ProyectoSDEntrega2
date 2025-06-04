from fastapi import FastAPI, HTTPException
from app.database import events_collection
from app.models import EventoReal
from bson import ObjectId
from datetime import datetime

app = FastAPI()

@app.post("/eventos")
async def crear_evento(evento: EventoReal):
    # Convertimos a dict y añadimos fecha de creación
    evento_data = evento.dict()
    evento_data["created_at"] = datetime.utcnow()
    
    result = events_collection.insert_one(evento_data)
    return {"id": str(result.inserted_id)}

@app.get("/eventos/getall")
async def obtener_eventos():
    eventos = []
    for evento in events_collection.find():
        evento["_id"] = str(evento["_id"])
        eventos.append(evento)
    return eventos  

@app.get("/eventos/{uuid}")
async def obtener_evento_por_uuid(uuid: str):
    evento = events_collection.find_one({"uuid": uuid})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    evento["_id"] = str(evento["_id"])
    return evento