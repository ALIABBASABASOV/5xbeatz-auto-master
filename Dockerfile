# 1. Python mühitini qururuq
FROM python:3.10-slim

# 2. Səs kitabxanalarını (libsndfile, ffmpeg) sistemə mühürləyirik
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 3. İş sahəsini yaradırıq
WORKDIR /app

# 4. Sənin o liyakatli fayllarını içəri köçürürük
COPY . .

# 5. Kitabxanaları quraşdırırıq
RUN pip install --no-cache-dir -r requirements.txt

# 6. Portu 7860-a mühürləyirik (Hugging Face üçün)
ENV PORT=7860
EXPOSE 7860

# 7. Sistemi işə salırıq
CMD ["python", "master_server.py"]