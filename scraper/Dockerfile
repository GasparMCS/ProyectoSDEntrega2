FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget curl gnupg libnss3 libxss1 libasound2 libatk1.0-0 libgtk-3-0 libx11-xcb1 libgbm1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils libu2f-udev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && playwright install --with-deps chromium

WORKDIR /app

COPY . /app

CMD ["python", "scraper.py"]