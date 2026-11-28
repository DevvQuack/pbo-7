# Materi PBO: class, enkapsulasi, instansiasi, asosiasi, abstraksi, SRP.
"""Class Penghuni berdiri sendiri; tidak mewarisi Orang."""

from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING
from .validasi import nomor_telepon_valid, teks_wajib

if TYPE_CHECKING:
    from .kamar import Kamar
    from .penyewaan import Penyewaan


# [CLASS, SRP] Mengelola identitas serta relasi sewa penghuni.
class Penghuni:
    # [CONSTRUCTOR, ENKAPSULASI] Atribut private untuk setiap instance.
    def __init__(self, id_penghuni: str, nama: str, no_telpon: str) -> None:
        self.__id_penghuni = teks_wajib(id_penghuni, "ID penghuni").upper()
        self.__nama = teks_wajib(nama, "Nama penghuni")
        self.__no_telpon = nomor_telepon_valid(no_telpon)
        # [ASOSIASI] Menyimpan referensi transaksi aktif atau None.
        self.__penyewaan_aktif: Penyewaan | None = None

    @property
    def id_penghuni(self) -> str:
        return self.__id_penghuni

    @property
    def nama(self) -> str:
        return self.__nama

    # [ENKAPSULASI] Perubahan nama melalui validasi.
    @nama.setter
    def nama(self, nilai: str) -> None:
        self.__nama = teks_wajib(nilai, "Nama penghuni")

    @property
    def no_telpon(self) -> str:
        return self.__no_telpon

    # [ENKAPSULASI] Perubahan telepon melalui validasi.
    @no_telpon.setter
    def no_telpon(self, nilai: str) -> None:
        self.__no_telpon = nomor_telepon_valid(nilai)

    @property
    def penyewaan_aktif(self) -> Penyewaan | None:
        return self.__penyewaan_aktif

    def informasi(self) -> str:
        status = "Sedang menyewa" if self.penyewaan_aktif else "Belum menyewa"
        return f"{self.id_penghuni} - {self.nama} ({self.no_telpon}) [{status}]"

    def sewa_kamar(self, kamar: Kamar, tanggal_masuk: str | date) -> Penyewaan:
        """Membuat transaksi antara satu penghuni dan satu kamar."""
        from .penyewaan import Penyewaan

        # [INSTANSIASI, ASOSIASI] Membuat transaksi dengan objek penghuni dan kamar.
        transaksi = Penyewaan(self, kamar, tanggal_masuk)
        transaksi.proses_penyewaan()
        return transaksi

    # [ABSTRAKSI] Mendelegasikan aturan pengakhiran kepada objek transaksi.
    def keluar_kamar(self, tanggal_keluar: str | date) -> Penyewaan:
        if self.__penyewaan_aktif is None:
            raise ValueError(f"Penghuni {self.id_penghuni} tidak memiliki sewa aktif.")
        transaksi = self.__penyewaan_aktif
        transaksi.proses_pengakhiran(tanggal_keluar)
        return transaksi

    # [ENKAPSULASI] Method internal (konvensi protected) untuk relasi transaksi.
    def _pasang_penyewaan(self, transaksi: Penyewaan) -> None:
        """Method internal yang dipakai class Penyewaan."""
        if self.__penyewaan_aktif is not None:
            raise ValueError(f"Penghuni {self.id_penghuni} masih menyewa kamar lain.")
        self.__penyewaan_aktif = transaksi

    def _lepas_penyewaan(self, transaksi: Penyewaan) -> None:
        if self.__penyewaan_aktif is not transaksi:
            raise ValueError("Relasi penghuni dan penyewaan tidak konsisten.")
        self.__penyewaan_aktif = None
