# Procesamiento de Incidentes con Apache Pig

Este servicio ejecuta un script de **Apache Pig** para analizar los incidentes
obtenidos desde el proceso de filtrado. El objetivo es generar estadísticas
básicas agrupando los incidentes por comuna, tipo y fecha.

La imagen Docker definida en `Dockerfile` instala **Apache Hadoop** y **Apache Pig**,
permitiendo ejecutar el script sin dependencias adicionales.

## Ejecución

1. Asegúrese de tener generado el archivo `eventos_filtrados.csv` en
   `servicios/filtro/output/`.
2. Desde esta carpeta puede ejecutarse el script con:

```bash
pig procesamiento.pig
```

Los resultados se guardarán en la carpeta `resultados/`.

## Uso con Docker

Puede construirse la imagen y ejecutarse mediante `docker-compose` desde la
carpeta `servicios`:

```bash
docker-compose run procesamiento
```
