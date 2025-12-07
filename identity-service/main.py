import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. VERİTABANI BAĞLANTISI AYARLARI
# Docker Compose'dan gelen adresi alıyoruz
DATABASE_URL = os.getenv("DATABASE_URL")

# Bağlantı motorunu oluştur
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. VERİTABANI TABLO MODELİ (ORM)
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # Gerçek hayatta şifreleri hash'lemelisin!

# Uygulama başlarken tabloları otomatik oluştur
Base.metadata.create_all(bind=engine)

# 3. FASTAPI UYGULAMASI
app = FastAPI()

# Veritabanı oturumu açıp kapatan yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# İstemciden gelecek veri modelleri
class UserSignup(BaseModel):
    username: str
    password: str

# --- ENDPOINTLER ---

@app.get("/")
def home():
    return {"service": "Identity Service", "db_status": "Connected"}

# KAYIT OL (Register)
@app.post("/register")
def register(user: UserSignup, db: Session = Depends(get_db)):
    # Böyle bir kullanıcı var mı kontrol et
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış")
    
    # Yeni kullanıcı oluştur ve kaydet
    new_user = UserDB(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Kullanıcı başarıyla oluşturuldu", "user_id": new_user.id}

# GİRİŞ YAP (Login)
@app.post("/login")
def login(user: UserSignup, db: Session = Depends(get_db)):
    # Veritabanında ara
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")
    
    return {"message": "Giriş Başarılı", "token": f"token-for-{db_user.username}"}