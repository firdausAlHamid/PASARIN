from fastapi import FastAPI, Request, Depends
import httpx
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import HTMLResponse

from app.database import engine, get_db
from app import models
from app.services.ocr_service import extract_receipt_data

# Menyuruh SQLAlchemy membuat tabel di MySQL (jika belum ada)
models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(title="PASARIN API")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Variabel penyimpan data sementara (State Management)
pending_transactions = {}

async def send_telegram_message(chat_id: int, text: str):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

@app.post("/webhook")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        
        # 1. PROSES FOTO
        if "photo" in data["message"]:
            await send_telegram_message(chat_id, "⏳ Sedang memproses struk dengan AI...")
            file_id = data["message"]["photo"][-1]["file_id"]
            
            async with httpx.AsyncClient() as client:
                file_info = await client.get(f"{TELEGRAM_API_URL}/getFile?file_id={file_id}")
                path = file_info.json()["result"]["file_path"]
                image_resp = await client.get(f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{path}")
                
                try:
                    result = extract_receipt_data(image_resp.content)
                    
                    # SIMPAN DATA SEMENTARA KE MEMORI
                    pending_transactions[chat_id] = result
                    
                    response_text = (
                        f"✅ **Struk Berhasil Dibaca!**\n\n"
                        f"🏪 Toko: {result.get('merchant')}\n"
                        f"💰 Total: Rp {result.get('total_amount'):,}\n"
                        f"📁 Kategori: {result.get('category')}\n"
                        f"📅 Tanggal: {result.get('date')}\n\n"
                        f"Ketik **SIMPAN** untuk mencatat transaksi ini."
                    )
                except Exception as e:
                    print(f"Error OCR: {e}")
                    response_text = "❌ Maaf, AI gagal membaca struk. Pastikan foto jelas."
            
            await send_telegram_message(chat_id, response_text)

        # 2. PROSES TEKS
        elif "text" in data["message"]:
            text_received = data["message"]["text"]
            first_name = data["message"]["chat"].get("first_name", "Pedagang")
            
            if text_received == "/start":
                user = db.query(models.User).filter(models.User.telegram_user_id == chat_id).first()
                if not user:
                    user = models.User(telegram_user_id=chat_id, owner_name=first_name, business_name=f"Toko {first_name}")
                    db.add(user); db.commit(); db.refresh(user)
                    reply = f"Halo {first_name}, pendaftaran berhasil! Mau catat apa hari ini?"
                else:
                    reply = f"Halo kembali, kak {first_name}! Tokomu '{user.business_name}' sudah siap."
                await send_telegram_message(chat_id, reply)
            
            # LOGIKA EKSEKUSI SIMPAN KE DATABASE
            elif text_received.upper() == "SIMPAN":
                if chat_id in pending_transactions:
                    data_to_save = pending_transactions[chat_id]
                    
                    # Cari ID user di database berdasarkan chat_id Telegram
                    user = db.query(models.User).filter(models.User.telegram_user_id == chat_id).first()
                    
                    if user:
                        try:
                            # Buat objek transaksi baru
                            new_trx = models.Transaction(
                                user_id=user.id,
                                transaction_type="expense", # Asumsi struk belanja = pengeluaran
                                amount=data_to_save['total_amount'],
                                category=data_to_save['category'],
                                description=f"Belanja di {data_to_save['merchant']}",
                                transaction_date=data_to_save['date']
                            )
                            # Simpan permanen ke MySQL
                            db.add(new_trx)
                            db.commit()
                            
                            # Hapus data dari memori sementara
                            del pending_transactions[chat_id]
                            
                            await send_telegram_message(chat_id, "💾 **Sukses!** Data transaksi telah dicatat ke database.")
                        except Exception as e:
                            print(f"Error Database: {e}")
                            await send_telegram_message(chat_id, "❌ Gagal menyimpan ke database. Cek format data.")
                    else:
                        await send_telegram_message(chat_id, "❌ Akunmu belum terdaftar. Ketik /start dulu ya.")
                else:
                    await send_telegram_message(chat_id, "🤔 Tidak ada struk yang sedang diproses. Silakan kirim foto struk terlebih dahulu.")
            
            else:
                await send_telegram_message(chat_id, f"Sistem menerima: '{text_received}'. Kirim foto struk untuk mulai mencatat.")

    return {"status": "ok"}

@app.get("/api/analytics/categories")
async def get_category_data(db: Session = Depends(get_db)):
    """API untuk mengambil total pengeluaran per kategori dari database"""
    results = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label("total")
    ).group_by(models.Transaction.category).all()
    
    # Format datanya menjadi list of dictionary agar mudah dibaca oleh JavaScript (JSON)
    return [{"category": r.category, "total": float(r.total)} for r in results]

@app.get("/api/transactions/recent")
async def get_recent_transactions(db: Session = Depends(get_db)):
    """API untuk mengambil 5 transaksi terbaru untuk tabel dashboard"""
    # Ambil 5 data terbaru dari database
    transactions = db.query(models.Transaction)\
        .order_by(models.Transaction.transaction_date.desc())\
        .limit(5).all()
    
    # Format data agar mudah dibaca oleh tabel HTML
    result = []
    for t in transactions:
        result.append({
            "date": t.transaction_date.strftime("%Y-%m-%d"),
            # Jika deskripsi kosong, tampilkan "Transaksi Tanpa Nama"
            "merchant": t.description if t.description else "Transaksi Tanpa Nama",
            "category": t.category,
            "amount": float(t.amount)
        })
    return result

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    """Rute untuk menampilkan file index.html di browser"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: File index.html tidak ditemukan!</h1>", status_code=404)