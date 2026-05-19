import gspread
import re

CREDENTIALS_FILE = "credentials.json" 

def extract_sheet_id(url_or_id):
    """Mengekstrak ID dari URL Google Sheets panjang yang dikirim UMKM"""
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_or_id)
    return match.group(1) if match else url_or_id

def append_to_sheet(sheet_url, date, tx_type, merchant, category, amount):
    if not sheet_url:
        return False
        
    try:
        # 1. Autentikasi ke Google Sheets
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        
        # 2. Ekstrak ID dan buka sheet
        sheet_id = extract_sheet_id(sheet_url)
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.sheet1
        
        # --- Buat Header Otomatis Jika Sheet Masih Kosong ---
        first_row = worksheet.row_values(1)
        if not first_row:
            headers = ["Tanggal", "Jenis Transaksi", "Merchant / Nama Toko", "Kategori pengeluaran", "Total Harga"]
            worksheet.append_row(headers)
            worksheet.format("A1:E1", {"textFormat": {"bold": True}})

        # 3. Masukkan data ke baris baru (Sesuai urutan header)
        jenis_transaksi = "Pengeluaran" if tx_type == "expense" else "Pemasukan"
        
        worksheet.append_row([date, jenis_transaksi, merchant, category, float(amount)])
        return True
        
    except Exception as e:
        print(f"Error Google Sheets: {e}")
        return False