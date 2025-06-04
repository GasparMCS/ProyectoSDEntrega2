# ProyectoSDEntrega2

Este repositorio contiene un conjunto de servicios Dockerizados para la captura, almacenamiento y procesamiento de eventos de **Waze Live Map**. Cada componente se encuentra en su propia carpeta con su respectivo `Dockerfile` y dependencias.

## Servicios principales

- **scraper**: utiliza Playwright para obtener eventos en tiempo real del mapa de Waze y los envía al servicio de almacenamiento.
- **almacenamiento**: API construida con FastAPI que persiste los eventos en MongoDB.
- **cache**: expone una API que consulta primero en Redis y, en caso de fallo, delega en el servicio de almacenamiento.
- **filtro**: descarga los eventos desde MongoDB, limpia la información y genera `eventos_filtrados.csv`.
- **procesamiento**: ejecuta un script de Apache Pig para obtener estadísticas a partir de los eventos filtrados.
- **generador_trafico**: realiza peticiones al servicio de cache siguiendo diferentes distribuciones para medir su desempeño.

## Ejecución rápida

1. Ajuste las variables del archivo `.env` para conectar con su instancia de MongoDB.
2. Construya las imágenes y levante los servicios:

```bash
docker-compose up --build
```

El scraper comenzará a enviar eventos y podrá consultarlos a través del servicio de almacenamiento o del cache.

Para lanzar el procesamiento de datos se puede ejecutar el contenedor `procesamiento` de forma aislada:

```bash
docker-compose run procesamiento
```

Los resultados quedarán en la carpeta `procesamiento/resultados/`.

Consulte la documentación específica de cada servicio dentro de su directorio para más detalles.
