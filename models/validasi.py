from datetime import date, datetime
import re

def teks_wajib(nilai: str, nama_field: str) -> str:
    if not isinstance(nilai, str) or not nilai.strip():
        raise ValueError(f"{nama_field} tidak boleh kosong.")
    return nilai.strip()

def nomor_telepon_valid(nomor: str) -> str:
    nomor = teks_wajib(nomor, "Nomor telepon")
    if not re.fullmatch(r"(?:|62|0)8\d{8,11}", nomor):
        raise ValueError("Nomor telepon harus seperti 081234567890 atau 6281234567890.")
    return nomor

def harga_valid(harga: int) -> int:
    if isinstance(harga, bool) or not isinstance(harga, int) or harga <= 0:
        raise ValueError("Harga sewa harus bilangan bulat lebih dari nol.")
    return harga

def tanggal_valid(nilai: str | date) -> date:
    if isinstance(nilai, datetime):
        raise ValueError("Tanggal tidak boleh memuat jam.")
    if isinstance(nilai, date):
        return nilai
    if not isinstance(nilai, str):
        raise ValueError("Tanggal harus dalam format YYYY-MM-DD.")
    try:
        tanggal = date.fromisoformat(nilai.strip())
    except ValueError as error:
        raise ValueError("Tanggal tidak valid. Gunakan format YYYY-MM-DD.") from error
    if tanggal.isoformat() != nilai.strip():
        raise ValueError("Tanggal harus dalam format YYYY-MM-DD.")
    return tanggal

def rupiah(nilai: int) -> str:
    return f"Rp{nilai:,}".replace(",", ".")
