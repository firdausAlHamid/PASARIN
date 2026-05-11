# Gunakan image Python versi ringan
FROM python:3.11-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Copy file requirements.txt lalu install library-nya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode proyekmu ke dalam container
COPY . .

# Ekspos port 8000 untuk FastAPI
EXPOSE 8000

# Perintah untuk menjalankan server Uvicorn saat container menyala
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]