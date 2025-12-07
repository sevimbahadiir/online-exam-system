# 1. Python'un hafif bir sürümünü temel al
FROM python:3.9-slim

# 2. Çalışma klasörünü ayarla
WORKDIR /app

# 3. Önce gereksinim dosyasını kopyala (Cache mantığı için önemli)
COPY requirements.txt .

# 4. Kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kalan kod dosyalarını kopyala
COPY . .

# 6. Dış dünyaya 8000 portunu açacağını söyle
EXPOSE 8000

# 7. Uygulamayı başlat (host 0.0.0.0 olmak zorunda, yoksa dışarıdan erişilemez)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]