from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Inisialisasi tanpa http_options terlebih dahulu untuk membiarkan SDK memilih default terbaik
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
        # Gunakan ID model lengkap: 'gemini-1.5-flash'
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            ]
        )
        
        # Log untuk debugging jika perlu melihat output mentah
        print("Raw AI Response:", response.text)
        
        raw_text = response.text.strip()
        # Pembersihan tag markdown JSON jika ada
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_text)
        
    except Exception as e:
        # Jika masih 404, kita coba fallback ke model 'gemini-1.5-flash-latest'
        print(f"Gagal dengan flash, mencoba flash-latest... Error: {e}")
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash-latest",
                contents=[prompt, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
            )
            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            return json.loads(raw_text)
        except Exception as e2:
            print(f"Semua model gagal: {e2}")
            raise e2