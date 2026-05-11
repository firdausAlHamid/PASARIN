# PASARIN

PASARIN adalah platform pencatatan usaha berbasis Telegram yang dirancang untuk membantu pedagang, UMKM, dan pelaku usaha secara umum dalam mengelola aktivitas bisnis sehari-hari. Platform ini menyediakan fitur pencatatan transaksi, pengingat jadwal seperti jatuh tempo utang/piutang, dashboard analitik berbasis web, serta insight bisnis berbasis AI untuk mendukung pengambilan keputusan usaha yang lebih tepat dan efisien.

## Fitur Utama

- **OCR Struk Otomatis**: Menggunakan **Gemini 2.5 Flash** untuk membaca total belanja, kategori, merchant, dan tanggal dari foto struk.
- **Manajemen Transaksi**: Menyimpan data pengeluaran secara permanen ke database MySQL.
- **Dashboard Analitik**: Visualisasi data real-time menggunakan FastAPI dan Chart.js dengan tema _Dark Mode_ yang intuitif.
- **Onboarding Telegram**: Sistem pendaftaran pengguna otomatis saat pertama kali memulai bot.

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: MySQL, SQLAlchemy (ORM)
- **AI/OCR**: Google Gemini AI (Generative AI SDK)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Bot Platform**: Telegram Bot API
- **Infrastruktur**: Docker & Docker Compose
- **Tunneling**: Ngrok (untuk webhook lokal)

## Prasyarat

Karena proyek ini sudah menggunakan **Docker**, Anda tidak perlu lagi menginstal Python atau MySQL (XAMPP) secara manual. Pastikan Anda hanya memiliki:

- **Docker Desktop** (atau Docker Engine & Docker Compose) yang sudah berjalan.
- Akun Google AI Studio (untuk Gemini API Key).
- Bot Telegram (dibuat via @BotFather).
- Ngrok.

## Instalasi & Setup

1.  **Clone Repositori**

    ```bash
    git clone https://github.com/firdausAlHamid/PASARIN.git
    cd PASARIN
    ```

2.  **Konfigurasi Environment Variable**
    Buat file `.env` di folder root (Anda bisa menyalin dari `.env.example`) dan pastikan isinya mencakup koneksi database untuk Docker:
    `````env
    TELEGRAM_BOT_TOKEN=isi_token_bot_anda
    GEMINI_API_KEY=isi_api_key_gemini_anda
    MYSQL_ROOT_PASSWORD=password_rahasia_anda # Pastikan host database mengarah ke 'db', BUKAN 'localhost'
    DATABASE_URL=mysql+pymysql://root:password_rahasia_anda@db:3306/pasarin_db
        ````
    `````

## Cara Menjalankan

1. **Jalankan Aplikasi dengan Docker**
   Jalankan perintah ini di terminal (pastikan Docker Desktop sudah menyala). Perintah ini otomatis akan mengunduh Python, MySQL, menginstal library, dan menyalakan server FastAPI:

   ```bash
   docker-compose up -d --build

   ```

_(Catatan: Tabel database akan otomatis terbuat saat container web berjalan pertama kali)._

2. **Jalankan Ngrok (Terminal Terpisah)**

   ```bash
   ngrok http 8000

   ```

3. **Set Webhook Telegram**
   Buka browser dan akses URL berikut (ganti `<TOKEN_BOT>` dan `<URL_NGROK>` dengan data Anda):
   `https://api.telegram.org/bot<TOKEN_BOT>/setWebhook?url=<URL_NGROK>/webhook`
4. **Akses Dashboard & Database**

- **Dashboard Web**: Buka browser di alamat `http://localhost:8000/dashboard`
- **Manajemen Database**: Gunakan Database Client (seperti DBeaver / VS Code / DataGrip) dengan koneksi Host: `127.0.0.1`, Port: `3306`, User: `root`, dan Password sesuai isi file `.env` Anda.

## Menghentikan Aplikasi

Jika ingin mematikan aplikasi dan database, cukup jalankan:

    ```bash
    docker-compose down

    ```

## Struktur Proyek

```text
PASARIN/
├── app/                    # Folder pusat aplikasi Python
│   ├── __init__.py
│   ├── main.py             # Logic utama Bot & API FastAPI
│   ├── database.py         # Konfigurasi koneksi Database
│   ├── models.py           # Skema tabel Database
│   └── services/           # Folder khusus AI, OCR, dan Machine Learning
│       ├── __init__.py
│       └── ocr_service.py  # Integrasi Google Gemini AI (OCR)
├── templates/              # Folder khusus tampilan UI/Frontend
│   └── index.html
├── scripts/                # Folder untuk script tambahan/testing
│   └── cek_model.py
├── venv/                   # (Diabaikan oleh Git, opsional jika ingin test lokal)
├── .env                    # Kredensial rahasia (Diabaikan oleh Git)
├── .env.example
├── .gitignore
├── docker-compose.yml      # Konfigurasi container Docker
├── Dockerfile              # Resep container Python FastAPI
├── README.md
└── requirements.txt

```
