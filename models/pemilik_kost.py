from validasi import nomor_telepon_valid, teks_wajib


class PemilikKost:
    def __init__(self, id_pemilik: str, nama: str, no_telpon: str) -> None:
        self.__id_pemilik = teks_wajib(id_pemilik, "ID pemilik").upper()
        self.__nama = teks_wajib(nama, "Nama pemilik")
        self.__no_telpon = nomor_telepon_valid(no_telpon)

    @property
    def id_pemilik(self) -> str:
        return self.__id_pemilik

    @property
    def nama(self) -> str:
        return self.__nama

    @nama.setter
    def nama(self, nilai: str) -> None:
        self.__nama = teks_wajib(nilai, "Nama pemilik")

    @property
    def no_telpon(self) -> str:
        return self.__no_telpon

    @no_telpon.setter
    def no_telpon(self, nilai: str) -> None:
        self.__no_telpon = nomor_telepon_valid(nilai)

    def informasi(self) -> str:
        return f"{self.__id_pemilik} - {self.__nama} ({self.__no_telpon})"

    def __str__(self) -> str:
        return self.informasi()
