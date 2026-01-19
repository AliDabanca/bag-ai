# 1. BAZ İMAJ: Python kurulu hafif bir Linux (Slim) versiyonu indir.
# (Sanki boş temiz bir bilgisayar kiralıyormuşsun gibi düşün)
FROM python:3.11-slim

# 2. ÇALIŞMA KLASÖRÜ: Konteynerin içinde /app diye bir klasör aç ve içine gir.
WORKDIR /app

# 3. DOSYALARI KOPYALA: Senin bilgisayarındaki (.) tüm dosyaları
# Konteynerin içindeki (.) /app klasörüne kopyala.
COPY . .

# 4. KURULUM: requirements.txt içindeki kütüphaneleri (FastAPI, Uvicorn) yükle.
# --no-cache-dir: Gereksiz önbellek dosyalarını tutma ki imajın boyutu küçük olsun.
RUN pip install --no-cache-dir -r requirements.txt

# 5. BAŞLAT: Konteyner çalıştığında bu komutu çalıştır.
# --host 0.0.0.0: Dışarıdan gelen isteklere açık ol demek.
# --port 8000: 8000 portunu kullan.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]