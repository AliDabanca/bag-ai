import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from dotenv import load_dotenv
# YENİ KÜTÜPHANE:
from huggingface_hub import AsyncInferenceClient 

load_dotenv()

# HuggingFace Ayarları
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
# Resmi istemciyi (Client) başlatıyoruz
client = AsyncInferenceClient(token=HF_TOKEN)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Veritabanı oturumu açıp kapatan yardımcı fonksiyon (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Ekleme (POST) - Yeni Çanta Ekle
@app.post("/cantalar/")
def canta_ekle(model: str, fiyat: int, renk: str, db: Session = Depends(get_db)):
    yeni_canta = models.Canta(model=model, fiyat=fiyat, renk=renk)
    db.add(yeni_canta)
    db.commit()
    db.refresh(yeni_canta)
    return yeni_canta

# 2. Listeleme (GET) - Tüm Çantaları Getir
@app.get("/cantalar/")
def cantalari_getir(db: Session = Depends(get_db)):
    return db.query(models.Canta).all()

@app.get("/oneri/")
async def akilli_oneri(mesaj: str, db: Session = Depends(get_db)):
    print(f"1. Kullanıcıdan gelen mesaj: {mesaj}") # LOG

    cantalar = db.query(models.Canta).all()
    if not cantalar:
        return {"hata": "Hiç çanta yok, önce veri ekle."}

    canta_isimleri = [c.model for c in cantalar]
    print(f"2. Çanta listesi hazırlandı: {len(canta_isimleri)} adet çanta var.") # LOG

    try:
        print("3. Yapay zekaya soruluyor... (Biraz bekle)") # LOG
        
        # HuggingFace'e istek atıyoruz
        sonuclar = await client.sentence_similarity(
            model="sentence-transformers/all-MiniLM-L6-v2",
            sentence=mesaj,
            other_sentences=canta_isimleri
        )
        
        print("4. Yapay zekadan cevap geldi! 🎉") # LOG
        
        en_yuksek_puan = max(sonuclar)
        en_iyi_indeks = sonuclar.index(en_yuksek_puan)
        kazanan_canta = cantalar[en_iyi_indeks]

        return {
            "kullanici_dedi_ki": mesaj,
            "yapay_zeka_onerdi": kazanan_canta.model,
            "guven_puani": float(en_yuksek_puan),
            "detaylar": kazanan_canta
        }

    except Exception as e:
        print(f"HATA OLUŞTU: {e}") # LOG
        return {"hata": "Yapay zeka bağlanamadı", "detay": str(e)}