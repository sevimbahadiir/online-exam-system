# Online Exam System - Deployment Guide

## Ön Gereksinimler
- Docker Desktop kurulu olmalı
- Kubernetes (minikube veya Docker Desktop'ta enable edilmiş)
- kubectl kurulu olmalı

## 1. Docker Image'ları Build Etme
```bash
# Her servisi build et
docker build -t sevimbahadiroglu/identity-service:latest ./identity-service
docker build -t sevimbahadiroglu/exam-service:latest ./exam-service
docker build -t sevimbahadiroglu/submit-service:latest ./submit-service
docker build -t sevimbahadiroglu/grading-service:latest ./grading-service

# Docker Hub'a push et (opsiyonel)
docker push sevimbahadiroglu/identity-service:latest
docker push sevimbahadiroglu/exam-service:latest
docker push sevimbahadiroglu/submit-service:latest
docker push sevimbahadiroglu/grading-service:latest
```

## 2. Kubernetes'e Deploy Etme
```bash
# Namespace'leri oluştur
kubectl apply -f k8s/all-in-one.yaml

# Prometheus'u düzelt
kubectl apply -f k8s/prometheus-fixed.yaml

# Grafana'yı deploy et
kubectl apply -f k8s/grafana.yaml

# Ingress'i deploy et (opsiyonel)
kubectl apply -f k8s/ingress.yaml

# Pod'ların çalıştığını kontrol et
kubectl get pods -n online-exam
kubectl get pods -n monitoring
```

## 3. Servislere Erişim

### Servisler:
- Identity Service: http://localhost:8000
- Exam Service: http://localhost:8001
- Submit Service: http://localhost:8002
- RabbitMQ Management: http://localhost:15672

### Monitoring:
- Prometheus: http://localhost:30090
- Grafana: http://localhost:30300 (admin/admin)

## 4. Grafana Dashboard Kurulumu

1. http://localhost:30300 adresine git
2. admin/admin ile giriş yap
3. Configuration → Data Sources → Add Prometheus
4. URL: `http://prometheus:9090`
5. Save & Test
6. Dashboard → Import → `online_exam_dashboard.json` dosyasını yükle

## 5. JMeter ile Test
```bash
# JMeter GUI ile test planını aç
jmeter -t jmeter/test-plan.jmx

# Headless mod ile çalıştır
jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/report
```

## Troubleshooting

### Pod çalışmıyorsa:
```bash
kubectl describe pod <pod-name> -n online-exam
kubectl logs <pod-name> -n online-exam
```

### Metrics görünmüyorsa:
```bash
# Servisin metrics endpoint'ini test et
kubectl port-forward svc/identity-service 8000:8000 -n online-exam
curl http://localhost:8000/metrics
```