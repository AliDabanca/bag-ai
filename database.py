import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# .env dosyasını yükle (Localde çalışırken şifreyi buradan okur)
load_dotenv()

# Şifreyi işletim sisteminden iste
# Eğer bulamazsa hata vermesin diye ikinci parametre boş string
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Bağlantı motorunu oluştur
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()