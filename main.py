from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Veritabanı tablolarını oluştur (Eğer yoksa)
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