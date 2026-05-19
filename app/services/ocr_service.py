from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
import time # <--- Tambahkan library time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_receipt_data(image_bytes: bytes):
    prompt = """
    Analisis gambar struk belanja ini. Ekstrak informasi berikut dalam format JSON:
    - total_amount: (angka saja, contoh 50000)
    - category: (pilih satu: Bahan Baku, Operasional, Gaji, atau Lainnya)
    - date: (format YYYY-MM-DD)
    - merchant: (nama toko)
    
    Hanya berikan JSON-nya saja, tanpa teks tambahan.
    """
    
    try:
        # Percobaan Pertama: Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            ]
        )
        
        raw_text = response.text.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_text)
        
    except Exception as e:
        print(f"Percobaan pertama gagal (Error: {e}). Menunggu 2 detik untuk mencoba lagi...")
        time.sleep(2) # Jeda 2 detik agar server Google tidak mengira kita spam
        
        try:
            # Percobaan Kedua: Fallback ke Gemini 1.5 Flash (tanpa tulisan -latest)
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
            )
            
            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            return json.loads(raw_text)
            
        except Exception as e2:
            print(f"Kedua model gagal: {e2}")
            raise e2