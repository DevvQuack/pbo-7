from validasi import harga_valid, teks_wajib

class Kamar:
    def __init__(self, nomor_kamar: str, tipe: str, harga_sewa: int) -> None:
        # Enkapsulasi: atribut private dan validasi saat objek dibuat.
        self.__nomor_kamar = teks_wajib(nomor_kamar, "Nomor kamar").upper()
        self.__tipe = teks_wajib(tipe, "Tipe kamar")
        self.__harga_sewa = harga_valid(harga_sewa)
        self.__status = "tersedia"

    @property
    def nomor_kamar(self) -> str:
        return self.__nomor_kamar

    @property
    def tipe(self) -> str:
        return self.__tipe

    @tipe.setter
    def tipe(self, nilai: str) -> None:
        self.__tipe = teks_wajib(nilai, "Tipe kamar")

    @property
    def harga_sewa(self) -> int:
        return self.__harga_sewa

    @harga_sewa.setter
    def harga_sewa(self, nilai: int) -> None:
        self.__harga_sewa = harga_valid(nilai)

    @property
    def status(self) -> str:
        return self.__status

    def tersedia(self) -> bool:
        return self.__status == "tersedia"

    def tempati(self) -> None:
        if not self.tersedia():
            raise ValueError(f"Kamar {self.nomor_kamar} tidak tersedia (sudah terisi).")
        self.__status = "terisi"

    def kosongkan(self) -> None:
        if self.tersedia():
            raise ValueError(f"Kamar {self.nomor_kamar} sudah kosong.")
            self.__status = "tersedia"

    def __str__(self) -> str:
        return f"Kamar {self.nomor_kamar} ({self.tipe}) - {self.status}"
