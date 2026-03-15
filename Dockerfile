FROM python:3.11-slim

# 1. Ses kütüphanelerini kur (Matchering ve Pedalboard için şart)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Kütüphaneleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Tüm projeyi içeri al
COPY . .

# 4. Gerekli klasörleri oluştur
RUN mkdir -p mastered temp

# 5. EN SAĞLAM BAŞLATMA KOMUTU
CMD ["uvicorn", "master_server:app", "--host", "0.0.0.0", "--port", "7860"]