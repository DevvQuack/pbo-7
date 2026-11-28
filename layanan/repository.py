# Materi PBO: abstraksi, abstract class, inheritance, overriding, enkapsulasi, SRP, OCP, ISP, DIP.
# LSP: implementasi diharapkan memenuhi kontrak; perlu uji perilaku transaksi nyata.
from abc import ABC, abstractmethod
from contextlib import contextmanager
from models.pemilik_kost import PemilikKost
from database.koneksi import Database


# [INHERITANCE] Exception khusus mewarisi RuntimeError.
class KesalahanPenyimpanan(RuntimeError):
    pass


# [ABSTRACT CLASS, ABSTRAKSI, DIP] Kontrak penyimpanan yang digunakan service.
class RepositoryKost(ABC):
    """Kontrak penyimpanan, tidak bergantung pada MySQL di service."""

    # [ABSTRACT METHOD] Subclass konkret wajib menyediakan operasi baca.
    @abstractmethod
    def baca(self):
        """Menghasilkan snapshot PemilikKost."""

    @abstractmethod
    def transaksi(self):
        """Context manager yang menghasilkan SesiKost dan commit/rollback."""


# [ABSTRACT CLASS, ISP] Kontrak operasi sesi terpisah dari pengelolaan repository.
class SesiKost(ABC):
    @abstractmethod
    def baca(self): ...

    @abstractmethod
    def tambah_kamar(self, kamar): ...

    @abstractmethod
    def tambah_penghuni(self, penghuni): ...

    @abstractmethod
    def mulai_sewa(self, transaksi): ...

    @abstractmethod
    def akhiri_sewa(self, transaksi): ...


# [INHERITANCE, SRP] Implementasi operasi SQL dalam sesi.
class SesiMySQL(SesiKost):
    def __init__(self, cursor):
        # [ENKAPSULASI] Atribut internal dengan konvensi satu garis bawah.
        self._cursor = cursor

    # [OVERRIDING, ABSTRAKSI] Mengubah baris database menjadi objek domain.
    def baca(self):
        c = self._cursor
        c.execute('SELECT nomor_kamar, tipe, harga_sewa FROM kamar ORDER BY nomor_kamar')
        kamar = c.fetchall()
        c.execute('SELECT id_penghuni, nama, no_telpon FROM penghuni ORDER BY id_penghuni')
        penghuni = c.fetchall()
        c.execute('SELECT id_penyewaan, id_penghuni, nomor_kamar, tanggal_masuk, tanggal_keluar FROM penyewaan ORDER BY id_penyewaan')
        return PemilikKost.dari_database(kamar, penghuni, c.fetchall())

    # [OVERRIDING] Menggunakan atribut objek dan SQL berparameter.
    def tambah_kamar(self, kamar):
        self._cursor.execute(
            'INSERT INTO kamar (nomor_kamar, tipe, harga_sewa) VALUES (%s, %s, %s)',
            (kamar.nomor_kamar, kamar.tipe, kamar.harga_sewa))

    def tambah_penghuni(self, penghuni):
        self._cursor.execute(
            'INSERT INTO penghuni (id_penghuni, nama, no_telpon) VALUES (%s, %s, %s)',
            (penghuni.id_penghuni, penghuni.nama, penghuni.no_telpon))

    def mulai_sewa(self, transaksi):
        self._cursor.execute(
            'INSERT INTO penyewaan (id_penghuni, nomor_kamar, tanggal_masuk) VALUES (%s, %s, %s)',
            (transaksi.penghuni.id_penghuni, transaksi.kamar.nomor_kamar, transaksi.tanggal_masuk))

    def akhiri_sewa(self, transaksi):
        self._cursor.execute(
            'UPDATE penyewaan SET tanggal_keluar = %s WHERE nomor_kamar = %s AND tanggal_keluar IS NULL',
            (transaksi.tanggal_keluar, transaksi.kamar.nomor_kamar))
        if self._cursor.rowcount != 1:
            raise KesalahanPenyimpanan('Transaksi aktif tidak ditemukan atau sudah berubah.')


# [INHERITANCE, SRP, OCP] Implementasi MySQL dari kontrak repository.
class RepositoryMySQL(RepositoryKost):
    # [DEPENDENCY INJECTION] Fungsi/method pembuat koneksi dapat diberikan dari luar.
    def __init__(self, koneksi=None):
        # [INSTANSIASI, ABSTRAKSI] Gunakan objek Database dan method koneksi().
        self._koneksi = koneksi if koneksi is not None else Database().koneksi

    @contextmanager
    def _sesi(self, tulis=False):
        from mysql.connector import Error, IntegrityError
        db = cursor = None
        try:
            # [INTERAKSI OBJEK] Memanggil method pembuat koneksi; koneksi baru per sesi.
            db = self._koneksi()
            cursor = db.cursor(dictionary=True)
            if tulis:
                # Serialisasi operasi tulis antar request aplikasi; lock dilepas
                # saat koneksi ditutup. UNIQUE di SQL juga mencegah sewa ganda.
                cursor.execute("SELECT GET_LOCK(CONCAT(DATABASE(), ':kost_write'), 10) AS terkunci")
                if cursor.fetchone()['terkunci'] != 1:
                    raise KesalahanPenyimpanan('Database sedang sibuk. Coba lagi.')
            db.rollback()  # Named lock tetap dipegang sampai koneksi ditutup.
            db.start_transaction(isolation_level='REPEATABLE READ', consistent_snapshot=True)
            # [INSTANSIASI] Membuat objek sesi yang memenuhi kontrak SesiKost.
            yield SesiMySQL(cursor)
            db.commit()
        except IntegrityError as error:
            if db is not None:
                db.rollback()
            raise ValueError('Data bertentangan dengan aturan database (duplikat atau relasi tidak valid).') from error
        except Error as error:
            if db is not None:
                db.rollback()
            raise KesalahanPenyimpanan('Operasi MySQL gagal. Periksa koneksi dan konfigurasi database.') from error
        except Exception:
            if db is not None:
                db.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if db is not None:
                db.close()

    # [OVERRIDING] Implementasi kontrak pembacaan repository.
    def baca(self):
        with self._sesi() as sesi:
            return sesi.baca()

    def transaksi(self):
        return self._sesi(tulis=True)