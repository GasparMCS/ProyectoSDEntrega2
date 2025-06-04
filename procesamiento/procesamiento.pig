-- Usamos CSVLoader de Piggybank para manejar correctamente campos entre comillas
-- Registramos Piggybank directamente desde la ruta instalada en la imagen
REGISTER '/opt/pig/contrib/piggybank/java/piggybank.jar';
DEFINE CSVLoader org.apache.pig.piggybank.storage.CSVLoader();

incidentes = LOAD 'eventos_filtrados.csv'
    USING CSVLoader(',')
    AS (uuid:chararray, comuna:chararray, tipo:chararray, subtipo:chararray, fecha:chararray);

-- Filtrar datos no válidos
incidentes_filtrados = FILTER incidentes BY
    uuid != 'uuid' AND
    tipo IS NOT NULL AND comuna IS NOT NULL AND fecha IS NOT NULL;

-- Extraer solo la fecha (YYYY-MM-DD) desde el timestamp
incidentes_enriquecidos = FOREACH incidentes_filtrados GENERATE
    uuid, comuna, tipo, subtipo,
    SUBSTRING(fecha, 0, 10) AS dia;

-- Agrupar por comuna
agrupado_comuna = GROUP incidentes_enriquecidos BY comuna;
conteo_comuna = FOREACH agrupado_comuna GENERATE
    group AS comuna, COUNT(incidentes_enriquecidos) AS total_incidentes;

-- Agrupar por tipo
agrupado_tipo = GROUP incidentes_enriquecidos BY tipo;
conteo_tipo = FOREACH agrupado_tipo GENERATE
    group AS tipo, COUNT(incidentes_enriquecidos) AS total_por_tipo;

-- Agrupar por fecha
agrupado_fecha = GROUP incidentes_enriquecidos BY dia;
conteo_fecha = FOREACH agrupado_fecha GENERATE
    group AS fecha, COUNT(incidentes_enriquecidos) AS total_por_dia;

-- Agrupar por comuna y fecha (opcional)
comuna_fecha = FOREACH incidentes_enriquecidos GENERATE comuna, dia;
agrupado_comuna_fecha = GROUP comuna_fecha BY (comuna, dia);
conteo_comuna_fecha = FOREACH agrupado_comuna_fecha GENERATE
    group.comuna, group.dia, COUNT(comuna_fecha) AS total;

-- Guardar resultados
rmf resultados/conteo_comuna;
rmf resultados/conteo_tipo;
rmf resultados/conteo_fecha;
rmf resultados/conteo_comuna_fecha;
STORE conteo_comuna INTO 'resultados/conteo_comuna' USING PigStorage(',');
STORE conteo_tipo INTO 'resultados/conteo_tipo' USING PigStorage(',');
STORE conteo_fecha INTO 'resultados/conteo_fecha' USING PigStorage(',');
STORE conteo_comuna_fecha INTO 'resultados/conteo_comuna_fecha' USING PigStorage(',');