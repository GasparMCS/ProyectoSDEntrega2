import time
import random
import numpy as np
import requests
import argparse

# Argumentos CLI: duración, distribución, tasa
parser = argparse.ArgumentParser()
parser.add_argument("--duracion", type=int, default=1, help="Duración en minutos")
parser.add_argument("--distribucion", type=str, choices=["poisson", "uniforme"], default="poisson", help="Tipo de distribución")
parser.add_argument("--tasa", type=float, default=1.0, help="Tasa promedio (λ) de consultas por segundo")
args = parser.parse_args()


BASE_URL = "http://cache:8001"
ID_URL = "http://almacenamiento:8000/eventos/getall"  
EVENTO_URL = f"{BASE_URL}/eventos"

# Métricas
hits = 0
misses = 0
tiempos = []

# Obtener IDs válidos
resp = requests.get(ID_URL)
print("Respuesta de getall_ids:", resp.text)
try:
    data = resp.json()
    if isinstance(data, list):
        ids = [item["uuid"] for item in data if "uuid" in item]
    else:
        ids = data["ids"]
except Exception as e:
    print("No se pudieron obtener los IDs. Error:", e)
    exit(1)

# Tiempo límite de ejecución
fin = time.time() + args.duracion * 60

while time.time() < fin:
    evento_id = random.choice(ids)
    url = f"{EVENTO_URL}/{evento_id}"
    
    inicio = time.time()
    resp = requests.get(url)
    duracion = time.time() - inicio
    tiempos.append(duracion)

    if resp.ok:
        # El servicio cache responde con {"message": "CACHE"|"STORAGE", "evento": ...}
        origen = resp.json().get("message", "")
        if origen == "CACHE":
            hits += 1
        else:
            misses += 1
    else:
        print(f"Error consultando {evento_id}: {resp.status_code}")

    # Pausa basada en distribución elegida
    if args.distribucion == "poisson":
        pausa = min(np.random.exponential(1.0 / args.tasa), 0.2)  # Cap a 200 ms
    elif args.distribucion == "uniforme":
        pausa = np.random.uniform(0.01, 0.1)
    else:
        pausa = 1
    time.sleep(pausa)

# Resultados
total = hits + misses
print("\n--- Estadísticas ---")
print(f"Total consultas: {total}")
print(f"Cache HITs: {hits} ({(hits/total)*100:.2f}%)")
print(f"Cache MISSes: {misses}")
print(f"Tiempo promedio de respuesta: {sum(tiempos)/total:.4f} s")