# 1. Base image
FROM python:3.11-slim

# 2. Ortam değişkenleri (Kurulum sırasında hata almamak ve Python'u optimize etmek için)
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# 3. Sistemsel bağımlılıklar
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Çalışma dizini
WORKDIR /app

# 5. Bağımlılıkları kur
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Proje dosyalarını kopyala
COPY . .

# 7. İzinleri ayarla ve klasörleri oluştur
# Kullanıcı yetki sorunlarını aşmak için tüm dosyalar için izinleri genişletiyoruz
RUN mkdir -p /app/mastered /app/temp && \
    chmod -R 777 /app/mastered /app/temp

# 8. Çalıştırma komutu
# master_server:app kısmını kendi ana dosya adınla değiştirmeyi unutma
CMD ["uvicorn", "master_server:app", "--host", "0.0.0.0", "--port", "7860"]
