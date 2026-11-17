from datetime import date, datetime

class Validator:
    """Kelas utilitas dengan tanggung jawab tunggal untuk validasi data input."""

    @staticmethod
    def validasi_teks(nilai: str, nama_field: str) -> str:
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError(f"{nama_field} tidak boleh kosong.")
        return nilai.strip()

    @staticmethod
    def validasi_nomor_telepon(no_telpon: str) -> str:
        bersih = Validator.validasi_teks(no_telpon, "Nomor telepon")
        bersih = bersih.replace(" ", "").replace("-", "")

        if bersih.startswith("+"):
            angka = bersih[1:]
        else:
            angka = bersih

        if not angka.isdigit() or not (10 <= len(angka) <= 15):
            raise ValueError(
                "Nomor telepon tidak valid (harus berupa 10-15 digit angka)."
            )
        return bersih

    @staticmethod
    def validasi_harga_positif(harga: int) -> int:
        if isinstance(harga, bool) or not isinstance(harga, (int, float)):
            raise ValueError("Harga sewa harus berupa angka.")
        harga_int = int(harga)
        if harga_int <= 0:
            raise ValueError("Harga sewa harus bernilai positif (lebih dari 0).")
        return harga_int

    @staticmethod
    def validasi_tanggal(tanggal_str: str) -> date:
        teks = Validator.validasi_teks(tanggal_str, "Tanggal")
        try:
            return datetime.strptime(teks, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError(
                "Format tanggal tidak valid. Gunakan format YYYY-MM-DD (contoh: 2026-11-17)."
            ) from exc

    @staticmethod
    def validasi_urutan_tanggal(tanggal_masuk: date, tanggal_keluar: date) -> None:
        if tanggal_keluar < tanggal_masuk:
            raise ValueError(
                "Tanggal keluar tidak boleh lebih awal dari tanggal masuk."
            )