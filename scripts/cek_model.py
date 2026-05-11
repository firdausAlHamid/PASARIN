import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Daftar model yang bisa kamu gunakan:")
print("-" * 40)

try:
    # Meminta daftar model dari server Google
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print("Gagal mengambil daftar model:", e)