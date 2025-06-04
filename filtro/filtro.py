import pandas as pd
from pymongo import MongoClient
from geopy.distance import geodesic
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") 

def obtener_eventos():
    client = MongoClient(MONGO_URI)
    db = client[os.getenv("MONGO_DB")] 
    collection = db[os.getenv("MONGO_COLLECTION")] 
    eventos = list(collection.find())
    return pd.DataFrame(eventos)

def filtrar_eventos(df):
    """Limpia y prepara los eventos obtenidos de MongoDB."""

    # Extraer latitud y longitud desde el campo "location"
    df["lat"] = df["location"].apply(
        lambda loc: loc.get("y") if isinstance(loc, dict) else None
    )
    df["lng"] = df["location"].apply(
        lambda loc: loc.get("x") if isinstance(loc, dict) else None
    )

    # Identificador único
    df["uuid"] = df.get("uuid")

    # Campos principales
    df["city"] = df.get("city")
    df["type"] = df.get("type")
    df["subtype"] = df.get("subtype")

    # Convertir pubMillis (ms) a timestamp ISO 8601 (UTC)
    df["timestamp"] = pd.to_datetime(
        df.get("pubMillis"), unit="ms", utc=True
    ).dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Considerar cadenas vacías como valores faltantes
    df.replace("", pd.NA, inplace=True)

    # Eliminar registros con datos esenciales faltantes
    df = df.dropna(
        subset=["lat", "lng", "uuid", "city", "type", "subtype", "timestamp"]
    )

    # Quitar duplicados por UUID
    df = df.drop_duplicates(subset="uuid")
    return df

def agrupar_eventos(df):
    """Agrupa por ciudad, tipo y tiempo para eliminar duplicados."""

    columnas = ["city", "type", "subtype", "timestamp"]
    df = df.sort_values("timestamp")
    agrupado = df.groupby(columnas, as_index=False).first()
    return agrupado

def exportar_csv(
    df,
    nombre_archivo="/app/output/eventos_filtrados.csv",
):
    """Guarda el CSV en la ruta compartida con el host."""

    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
    columnas = ["uuid", "city", "type", "subtype", "timestamp"]
    df[columnas].to_csv(nombre_archivo, index=False)
    print(f"Archivo exportado: {nombre_archivo}")

if __name__ == "__main__":
    df = obtener_eventos()
    print(f"Original: {len(df)} eventos")

    df = filtrar_eventos(df)
    print(f"Filtrados: {len(df)} eventos")

    df = agrupar_eventos(df)
    print(f"Agrupados: {len(df)} eventos")

    exportar_csv(df)