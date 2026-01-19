from fastapi import FastAPI

# Uygulamayı yaratıyoruz (Dükkanın kepengini takmak gibi)
app = FastAPI()

# SAHTE VERİTABANI
# Normalde burası veritabanından gelir ama şimdilik elimizle yazalım.
# Bu bir Python Listesi içinde Sözlükler (Dictionary)
canta_stoklari = [
    {"id": 1, "model": "Deri Sırt Çantası", "fiyat": 1500, "renk": "Siyah"},
    {"id": 2, "model": "Laptop Çantası", "fiyat": 2000, "renk": "Gri"},
    {"id": 3, "model": "Spor Çanta", "fiyat": 800, "renk": "Mavi"}
]

# 1. Endpoint (Anasayfa)
# Biri senin sitene (/) girdiğinde ne desin?
@app.get("/")
def ana_sayfa():
    return {"mesaj": "Çanta Dükkanına Hoşgeldiniz!"}

# 2. Endpoint (Ürünleri Listele)
# Biri "/cantalar" adresine gittiğinde ne görsün?
@app.get("/cantalar")
def cantalari_getir():
    # Python sözlüğünü (dictionary) olduğu gibi döndürüyoruz.
    # FastAPI bunu otomatik olarak JSON'a çevirecek.
    return canta_stoklari

# 3. Endpoint (Özel Arama)
# Biri "/cantalar/1" derse sadece 1 numaralı çantayı görsün.
@app.get("/cantalar/{canta_id}")
def tek_canta_getir(canta_id: int):
    # Basit bir döngü ile o ID'ye sahip çantayı bulalım
    for canta in canta_stoklari:
        if canta["id"] == canta_id:
            return canta
    return {"hata": "Böyle bir çanta bulunamadı"}