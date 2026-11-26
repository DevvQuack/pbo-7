# Materi PBO: class, constructor, atribut instance, enkapsulasi, abstraksi, SRP.
"""Class Kamar: menyimpan data kamar dan menjaga status tersedia/terisi."""

from .validasi import harga_valid, teks_wajib


# [CLASS, SRP] Mengelola data dan status kamar, bukan SQL atau HTML.
class Kamar:
    # [CONSTRUCTOR] Inisialisasi atribut setiap objek.
    def __init__(self, nomor_kamar: str, tipe: str, harga_sewa: int) -> None:
        # Enkapsulasi: atribut private dan validasi saat objek dibuat.
        self.__nomor_kamar = teks_wajib(nomor_kamar, "Nomor kamar").upper()
        self.__tipe = teks_wajib(tipe, "Tipe kamar")
        self.__harga_sewa = harga_valid(harga_sewa)
        self.__status = "tersedia"

    # [ENKAPSULASI] Getter tanpa setter; nomor kamar hanya dibaca lewat API publik.
    @property
    def nomor_kamar(self) -> str:
        return self.__nomor_kamar

    @property
    def tipe(self) -> str:
        return self.__tipe

    # [ENKAPSULASI] Setter memvalidasi perubahan tipe.
    @tipe.setter
    def tipe(self, nilai: str) -> None:
        self.__tipe = teks_wajib(nilai, "Tipe kamar")

    @property
    def harga_sewa(self) -> int:
        return self.__harga_sewa

    # [ENKAPSULASI] Setter menolak harga tidak valid.
    @harga_sewa.setter
    def harga_sewa(self, nilai: int) -> None:
        self.__harga_sewa = harga_valid(nilai)

    @property
    def status(self) -> str:
        return self.__status

    def tersedia(self) -> bool:
        return self.__status == "tersedia"

    # [ABSTRAKSI] Pemanggil memakai method, bukan mengubah status langsung.
    def tempati(self) -> None:
        if not self.tersedia():
            raise ValueError(f"Kamar {self.nomor_kamar} tidak tersedia (sudah terisi).")
        self.__status = "terisi"

    def kosongkan(self) -> None:
        if self.tersedia():
            raise ValueError(f"Kamar {self.nomor_kamar} sudah kosong.")
        self.__status = "tersedia"

    # [METHOD KHUSUS] Representasi teks objek Kamar.
    def __str__(self) -> str:
        return f"Kamar {self.nomor_kamar} ({self.tipe}) - {self.status}"
