CREATE DATABASE IF NOT EXISTS db_kost CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE db_kost;

CREATE TABLE IF NOT EXISTS kamar (
    nomor_kamar VARCHAR(30) PRIMARY KEY,
    tipe VARCHAR(60) NOT NULL,
    harga_sewa BIGINT NOT NULL CHECK (harga_sewa > 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS penghuni (
    id_penghuni VARCHAR(30) PRIMARY KEY,
    nama VARCHAR(120) NOT NULL,
    no_telpon VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS penyewaan (
    id_penyewaan BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_penghuni VARCHAR(30) NOT NULL,
    nomor_kamar VARCHAR(30) NOT NULL,
    tanggal_masuk DATE NOT NULL,
    tanggal_keluar DATE NULL,

    -- NULL boleh berulang pada UNIQUE; hanya sewa aktif yang dibatasi.
    kamar_aktif VARCHAR(30) GENERATED ALWAYS AS (
        CASE WHEN tanggal_keluar IS NULL THEN nomor_kamar ELSE NULL END
    ) STORED,
    penghuni_aktif VARCHAR(30) GENERATED ALWAYS AS (
        CASE WHEN tanggal_keluar IS NULL THEN id_penghuni ELSE NULL END
    ) STORED,
    UNIQUE (kamar_aktif),
    UNIQUE (penghuni_aktif),
    FOREIGN KEY (id_penghuni) REFERENCES penghuni(id_penghuni),
    FOREIGN KEY (nomor_kamar) REFERENCES kamar(nomor_kamar),
    CHECK (tanggal_keluar IS NULL OR tanggal_keluar >= tanggal_masuk)
) ENGINE=InnoDB;
