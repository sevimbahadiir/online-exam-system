FROM python:3.9-slim

# Logların anında görünmesi için gerekli ayar
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Bu bir API olmadığı için port açmıyoruz (EXPOSE yok)
CMD ["python", "worker.py"]