FROM python:3.9-slim

WORKDIR /app

# Instalar certificados raíz para conexiones HTTPS/SSL
RUN apt-get update && apt-get install -y ca-certificates && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "filtro.py"]
