import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

# 1. VERİTABANI AYARLARI
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. VERİTABANI TABLOSU (Exams)
class ExamDB(Base):
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    teacher = Column(String)

# Tabloyu oluştur
Base.metadata.create_all(bind=engine)

# 3. UYGULAMA VE MODELLER
app = FastAPI()

# Pydantic Modeli (Veri alışverişi için)
class ExamCreate(BaseModel):
    title: str
    teacher: str

class ExamResponse(BaseModel):
    id: int
    title: str
    teacher: str
    
    class Config:
        orm_mode = True

# Veritabanı Oturumu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTLER ---

@app.get("/")
def home():
    return {"service": "Exam Service", "db_status": "Connected"}

# SINAV EKLE
@app.post("/exams", response_model=ExamResponse)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    new_exam = ExamDB(title=exam.title, teacher=exam.teacher)
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam

# SINAVLARI LİSTELE
@app.get("/exams", response_model=List[ExamResponse])
def get_exams(db: Session = Depends(get_db)):
    return db.query(ExamDB).all()