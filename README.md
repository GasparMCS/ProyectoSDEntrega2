# ProyectoSDEntrega2

Este repositorio agrupa varios servicios Dockerizados para capturar, almacenar y
procesar eventos obtenidos desde **Waze Live Map**.

## Prerrequisitos

- Docker
- Docker Compose

## Configuración inicial

1. Clone este repositorio.
2. Cree un archivo `.env` en la raíz y defina las credenciales de MongoDB:

   ```bash
   MONGO_USER=<usuario>
   MONGO_PASSWORD=<contraseña>
   MONGO_CLUSTER=<url_del_cluster>
   MONGO_DB=<base_de_datos>
   MONGO_COLLECTION=<colección>
   ```

## Puesta en marcha

Desde la carpeta del proyecto ejecute:

```bash
docker-compose up --build
```

- `scraper` comenzará a recolectar eventos.
- `almacenamiento` y `cache` expondrán las APIs en `localhost:8000` y `localhost:8001` respectivamente.

## Procesamiento de datos

Para generar estadísticas a partir de los eventos filtrados:

```bash
docker-compose run procesamiento
```

Los resultados se guardarán en `procesamiento/resultados/`.

## Generar tráfico de prueba (opcional)

```bash
docker-compose run generador
```

## Visualización con Kibana

Acceda a `http://localhost:5601` para inspeccionar los datos almacenados en
Elasticsearch (`http://localhost:9200`).
Ademas de esto para poblar el almacenamiento lo hicimos atravez de un script que esta en `/Visualizador/indexador.py` que toma los datos filtrados (/procesamieto) y los envia a elastic, y luego para visualizar los datos hay que ir a dashboard y crear una vista.

## Estructura del proyecto

- `scraper/`
- `almacenamiento/`
- `cache/`
- `filtro/`
- `procesamiento/`
- `generador_trafico/`
- `visualizador/`

Cada servicio contiene su propio `Dockerfile` y dependencias.
