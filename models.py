from sqlalchemy import Column, Integer, String
from database import Base

class Canta(Base):
    __tablename__ = "cantalar"  # Veritabanındaki tablo adı

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    fiyat = Column(Integer)
    renk = Column(String)