from fastapi import FastAPI, HTTPException
from cache import cache
import requests
import os

STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL", "http://almacenamiento:8000")
TTL = int(os.getenv("TTL_CACHE", 3600))

app = FastAPI()

@app.get("/eventos/{evento_id}", status_code=200)
async def leer_evento_cache(evento_id: str):
    cached_event = cache.get(evento_id)
    if cached_event:
        return {"message": "CACHE", "evento": cached_event}
    
    response = requests.get(f"{STORAGE_SERVICE_URL}/eventos/{evento_id}")
    if response.status_code == 200:
        evento = response.json()
        cache.set(evento_id, str(evento), ex=TTL)
        return {"message": "STORAGE", "evento": evento}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    else:
        raise HTTPException(status_code=500, detail="Error al consultar almacenamiento")

@app.get("/eventos", status_code=200)
async def listar_eventos_cache():
    cached_eventos = cache.get("eventos")
    if cached_eventos:
        return {"message": "CACHE", "eventos": eval(cached_eventos)}
    
    response = requests.get(f"{STORAGE_SERVICE_URL}/eventos")
    if response.status_code == 200:
        eventos = response.json()
        cache.set("eventos", str(eventos), ex=TTL)
        return {"message": "STORAGE", "eventos": eventos}
    else:
        raise HTTPException(status_code=500, detail="Error al consultar almacenamiento")
