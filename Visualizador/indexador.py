import csv
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

with open('procesamiento/eventos_filtrados.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        es.index(index="eventos_trafico", document=row)