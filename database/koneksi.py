import os

# [CLASS DAN SRP]
# Class Database bertanggung jawab atas konfigurasi dan pembuatan koneksi ke database MySQL.
class Database:
    # [CONSTRUCTOR]
    def __init__(self):

        # [ENKAPSULASI]
        # Konfigurasi disimpan dalam atribut private.
        self.__host = os.getenv('DB_HOST', '127.0.0.1')
        self.__port = int(os.getenv('DB_PORT', '3306'))
        self.__user = os.getenv('DB_USER', 'root')
        self.__password = os.getenv('DB_PASSWORD', '')
        self.__database = os.getenv('DB_NAME', 'db_kost')

    # [ABSTRAKSI]
    # Pengguna class cukup memanggil method koneksi() tanpa mengetahui detail konfigurasi MySQL.
    def koneksi(self):
        import mysql.connector
        
        return mysql.connector.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__database,
            connection_timeout=5,
            autocommit=False,
        )
