import pika
import json
import time

# RabbitMQ'nun açılmasını bekleme (Basit retry mantığı)
# Bazen RabbitMQ servisten daha geç açılır, hata almamak için.
time.sleep(10)

def calculate_score(answers):
    # Basit bir puanlama mantığı (Simülasyon)
    score = 0
    # Örn: Her soru 10 puan varsayalım
    for question, answer in answers.items():
        if answer == "a": # Doğru cevap 'a' olsun
            score += 10
    return score

def callback(ch, method, properties, body):
    print(" [x] Bir sinav kagidi alindi!")
    
    # Gelen mesajı JSON'dan çevir
    data = json.loads(body)
    student = data.get('student_name')
    answers = data.get('answers')
    
    print(f" ... {student} adli ogrencinin kagidi okunuyor ...")
    
    # Puanlama yap (Simülasyon: 2 saniye sürsün)
    time.sleep(2) 
    final_score = calculate_score(answers)
    
    print(f" [OK] Puanlama Bitti: {student} -> Puan: {final_score}")
    print(" --------------------------------------------------- ")

    # Mesajı kuyruktan silebilirsin (İşlendi onayı)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# RabbitMQ Bağlantısı
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Kuyruğu tekrar tanımla (Eğer yoksa oluşturur)
channel.queue_declare(queue='exam_submissions')

# Her seferinde sadece 1 mesaj al (Biri bitmeden diğerini alma)
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='exam_submissions', on_message_callback=callback)

print(' [*] Grading Service calisiyor. Mesajlar bekleniyor...')
channel.start_consuming()