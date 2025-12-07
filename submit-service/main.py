from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json

app = FastAPI()

# Gelen Cevap Modeli
class Submission(BaseModel):
    student_name: str
    exam_id: int
    answers: dict  # Örn: {"soru1": "a", "soru2": "c"}

# RabbitMQ Bağlantı Fonksiyonu
def send_to_queue(message_dict):
    # 1. RabbitMQ sunucusuna bağlan (Host adı docker-compose'dan geliyor: 'rabbitmq')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # 2. Kuyruğu oluştur (Eğer yoksa)
    channel.queue_declare(queue='exam_submissions')

    # 3. Mesajı gönder
    channel.basic_publish(
        exchange='',
        routing_key='exam_submissions',
        body=json.dumps(message_dict)
    )
    
    # 4. Bağlantıyı kapat
    connection.close()

@app.get("/")
def home():
    return {"service": "Submit Service", "status": "Ready to send messages"}

@app.post("/submit")
def submit_exam(submission: Submission):
    # Gelen veriyi sözlüğe çevir
    data = submission.dict()
    
    # Kuyruğa yolla
    send_to_queue(data)
    
    # Kullanıcıyı bekletmeden hemen cevap ver
    return {"message": "Sinaviniz alindi, arka planda degerlendirilecek.", "status": "Queued"}