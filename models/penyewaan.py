from __future__ import annotations
from datetime import date
from .kamar import Kamar
from .penghuni import Penghuni
from validasi import tanggal_valid


class Penyewaan:
    def __init__(
        self, penghuni: Penghuni, kamar: Kamar, tanggal_masuk: str | date
    ) -> None:
        if not isinstance(penghuni, Penghuni) or not isinstance(kamar, Kamar):
            raise TypeError("Penyewaan membutuhkan objek Penghuni dan Kamar.")
        self.__penghuni = penghuni
        self.__kamar = kamar
        self.__tanggal_masuk = tanggal_valid(tanggal_masuk)
        self.__tanggal_keluar: date | None = None
        self.__sudah_dimulai = False

    @property
    def penghuni(self) -> Penghuni:
        return self.__penghuni

    @property
    def kamar(self) -> Kamar:
        return self.__kamar

    @property
    def tanggal_masuk(self) -> date:
        return self.__tanggal_masuk

    @property
    def tanggal_keluar(self) -> date | None:
        return self.__tanggal_keluar

    @property
    def aktif(self) -> bool:
        return self.__sudah_dimulai and self.__tanggal_keluar is None

    def proses_penyewaan(self) -> None:
        if self.__sudah_dimulai:
            raise ValueError("Transaksi sudah pernah diproses.")
        if not self.kamar.tersedia():
            raise ValueError(f"Kamar {self.kamar.nomor_kamar} tidak tersedia.")
        if self.penghuni.penyewaan_aktif is not None:
            raise ValueError(f"Penghuni {self.penghuni.id_penghuni} masih menyewa.")
        self.kamar.tempati()
        self.penghuni._pasang_penyewaan(self)
        self.__sudah_dimulai = True

    def proses_pengakhiran(self, tanggal_keluar: str | date) -> None:
        keluar = tanggal_valid(tanggal_keluar)
        if not self.aktif:
            raise ValueError("Penyewaan tidak aktif atau sudah diakhiri.")
        if keluar < self.tanggal_masuk:
            raise ValueError("Tanggal keluar tidak boleh lebih awal dari tanggal masuk.")
        if self.kamar.tersedia() or self.penghuni.penyewaan_aktif is not self:
            raise ValueError("Status kamar/penghuni tidak konsisten.")
          
        self.kamar.kosongkan()
        self.penghuni._lepas_penyewaan(self)
        self.__tanggal_keluar = keluar

    def __str__(self) -> str:
        akhir = self.tanggal_keluar.isoformat() if self.tanggal_keluar else "Aktif"
        return f"{self.penghuni.nama} / {self.kamar.nomor_kamar}: {self.tanggal_masuk} - {akhir}"
