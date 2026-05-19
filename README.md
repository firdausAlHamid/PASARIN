# PASARIN
PASARIN adalah platform pencatatan usaha berbasis Telegram yang dirancang untuk membantu pedagang, UMKM, dan pelaku usaha secara umum dalam mengelola aktivitas bisnis sehari-hari. Platform ini menyediakan fitur pencatatan transaksi, OCR cerdas untuk membaca struk belanja, serta integrasi pencatatan otomatis langsung ke Google Sheets milik masing-masing pengguna (Multi-Tenant SaaS).

## Fitur Utama

- **OCR Struk Otomatis**: Menggunakan **Gemini 2.5 Flash** untuk membaca total belanja, kategori, merchant, dan tanggal dari foto struk dengan kemampuan _fallback_ dinamis.
- **Integrasi Google Sheets (SaaS)**: Pengguna dapat menyambungkan bot ke spreadsheet milik mereka sendiri untuk pembukuan otomatis berupa tabel rapi (dilengkapi _Auto-Header_).
- **Manajemen Transaksi**: Menyimpan data pengeluaran secara permanen ke database MySQL.
- **Dashboard Analitik**: Visualisasi data real-time menggunakan FastAPI dan Chart.js dengan tema _Dark Mode_ yang intuitif.
- **Onboarding Telegram**: Sistem pendaftaran pengguna otomatis saat pertama kali memulai bot.

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: MySQL, SQLAlchemy (ORM)
- **AI/OCR**: Google Gemini AI (Generative AI SDK)
- **Integrasi Pihak Ketiga**: Google Sheets API (`gspread`)
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Bot Platform**: Telegram Bot API
- **Infrastruktur**: Docker & Docker Compose
- **Tunneling**: Ngrok (untuk webhook lokal)

## Prasyarat

Karena proyek ini sudah menggunakan **Docker**, Anda tidak perlu lagi menginstal Python atau MySQL (XAMPP) secara manual. Pastikan Anda hanya memiliki:

- **Docker Desktop** (atau Docker Engine & Docker Compose) yang sudah berjalan.
- Akun Google AI Studio (untuk Gemini API Key).
- Bot Telegram (dibuat via @BotFather).
- File kredensial Google Cloud Service Account (`credentials.json`) yang sudah diaktifkan akses _Google Sheets API_ dan _Google Drive API_.
- Ngrok.

## Instalasi & Setup

1.  **Clone Repositori**

    ```bash
    git clone [https://github.com/firdausAlHamid/PASARIN.git](https://github.com/firdausAlHamid/PASARIN.git)
    cd PASARIN
    ```

2.  **Konfigurasi Environment Variable**
    Buat file `.env` di folder root (Anda bisa menyalin dari `.env.example`) dan pastikan isinya mencakup:

    ```env
    TELEGRAM_BOT_TOKEN=isi_token_bot_anda
    GEMINI_API_KEY=isi_api_key_gemini_anda
    MYSQL_ROOT_PASSWORD=password_rahasia_anda
    # Pastikan host database mengarah ke 'db', BUKAN 'localhost'
    DATABASE_URL=mysql+pymysql://root:password_rahasia_anda@db:3306/pasarin_db
    ```

3.  **Setup Kredensial Google Sheets**
    ### Langkah 1: Buat Akun Robot & Download Kuncinya
    
    - Buka browser dan pergi ke [Google Cloud Console](https://console.cloud.google.com/).
    - Buat Project baru.
    - Cari di kolom pencarian atas: **Google Sheets API**, lalu klik **Enable** (Aktifkan).
    - Cari lagi: **Google Drive API**, lalu klik **Enable** (Aktifkan).
    - Masuk ke menu **IAM & Admin > Service Accounts** (Buka sidebar menu kiri `☰` jika tersembunyi).
    - Klik **Create Service Account**, beri nama bebas (misal: `bot-pasarin`), lalu klik **Done**.
    - Klik akun/email Service Account yang baru saja dibuat tersebut, masuk ke tab **Keys**.
    - Klik **Add Key > Create new key > pilih JSON**, lalu klik **Create**.
    - File JSON akan otomatis ter-download ke laptopmu.

    ### Langkah 2: Pasang Kunci ke Proyek
    
    - Ganti nama file JSON yang baru saja kamu download menjadi **`credentials.json`** (pastikan menggunakan huruf kecil semua).
    - Pindahkan file `credentials.json` tersebut ke folder utama **PASARIN** (sejajar dengan file `docker-compose.yml` dan `.env`).
    
    ### Langkah 3: Dapatkan Email Robot Asli
    
    - Buka file `credentials.json` tadi menggunakan Notepad atau VS Code.
    - Cari baris yang bertuliskan `"client_email"`. Di sebelahnya akan ada email asli yang bentuknya panjang dan unik (contoh: `bot-pasarin@pasarin-12345.iam.gserviceaccount.com`).
    - **Copy** email asli tersebut.
    - Buka Google Sheets yang ingin digunakan oleh UMKM, lalu klik tombol **Share/Bagikan** di pojok kanan atas.
    - Masukkan email asli tersebut dan beri akses sebagai **Editor**, lalu simpan.

## Perintah Bot Telegram (Bot Commands)

Daftarkan perintah berikut melalui BotFather (`/setcommands`):

- `start` - Mendaftarkan toko atau menyapa bot
- `setsheet` - Hubungkan Google Sheets (Masukkan link spreadsheet)
- `simpan` - Konfirmasi penyimpanan data struk terakhir

## Cara Menjalankan

1. **Jalankan Aplikasi dengan Docker**
   Jalankan perintah ini di terminal (pastikan Docker Desktop sudah menyala). Perintah ini otomatis akan mengunduh Python, MySQL, menginstal _library_, dan menyalakan server FastAPI:
   ```bash
   docker-compose up -d --build
   ```

````

*(Catatan: Tabel database akan otomatis terbuat saat container web berjalan pertama kali).*

2. **Jalankan Ngrok (Terminal Terpisah)**
```bash
ngrok http 8000

````

3. **Set Webhook Telegram**
   Buka browser dan akses URL berikut (ganti `<TOKEN_BOT>` dan `<URL_NGROK>` dengan data Anda):
   `https://api.telegram.org/bot<TOKEN_BOT>/setWebhook?url=<URL_NGROK>/webhook`
4. **Akses Dashboard & Database**

- **Dashboard Web**: Buka browser di alamat `http://localhost:8000/dashboard`
- **Manajemen Database**: Gunakan Database Client (seperti DBeaver / VS Code) dengan koneksi Host: `127.0.0.1`, Port: `3306`, User: `root`, dan Password sesuai isi file `.env`.

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
│   └── services/           # Folder khusus Integrasi
│       ├── __init__.py
│       ├── ocr_service.py  # Integrasi Google Gemini AI
│       └── sheets_service.py # Integrasi Google Sheets API (gspread)
├── templates/              # Folder UI/Frontend
│   └── index.html
├── scripts/                # Folder script tambahan
│   └── cek_model.py
├── venv/
├── .env                    # Kredensial rahasia (Diabaikan oleh Git)
├── .env.example
├── .gitignore
├── credentials.json        # Kredensial Google Service Account (Diabaikan Git)
├── docker-compose.yml      # Konfigurasi container Docker
├── Dockerfile              # Resep container Python FastAPI
├── README.md
└── requirements.txt

```
