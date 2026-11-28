from flask import Flask, jsonify, render_template, request
from models.kamar import Kamar
from models.penghuni import Penghuni
from models.penyewaan import Penyewaan

app = Flask(__name__)

kamar_db: dict[str, Kamar] = {}
penghuni_db: dict[str, Penghuni] = {}
riwayat: list[Penyewaan] = []


def _kamar_json(k: Kamar) -> dict:
    penyewa = next(
        (p.penghuni.nama for p in riwayat if p.kamar is k and p.aktif), None
    )
    return {
        "nomor_kamar": k.nomor_kamar,
        "tipe": k.tipe,
        "harga_sewa": k.harga_sewa,
        "status": k.status,
        "penghuni": penyewa,
    }

def _penghuni_json(p: Penghuni) -> dict:
    aktif = p.penyewaan_aktif
    return {
        "id_penghuni": p.id_penghuni,
        "nama": p.nama,
        "no_telpon": p.no_telpon,
        "kamar_aktif": aktif.kamar.nomor_kamar if aktif else None,
    }

def _sewa_json(s: Penyewaan) -> dict:
    return {
        "id_penghuni": s.penghuni.id_penghuni,
        "nama": s.penghuni.nama,
        "nomor_kamar": s.kamar.nomor_kamar,
        "tanggal_masuk": s.tanggal_masuk.isoformat(),
        "tanggal_keluar": s.tanggal_keluar.isoformat() if s.tanggal_keluar else None,
        "aktif": s.aktif,
    }

@app.errorhandler(ValueError)
@app.errorhandler(TypeError)
def kesalahan_input(error):
    # Pesan ValueError dari models/ dikirim apa adanya ke browser.
    return jsonify({"error": str(error)}), 400

@app.get("/")
def beranda():
    return render_template("index.html")

@app.get("/api/kamar")
def daftar_kamar():
    return jsonify([_kamar_json(k) for k in kamar_db.values()])

@app.post("/api/kamar")
def tambah_kamar():
    data = request.get_json(silent=True) or {}
    try:
        harga = int(data.get("harga_sewa"))
    except (TypeError, ValueError):
        raise ValueError("Harga sewa harus bilangan bulat lebih dari nol.")
    kamar = Kamar(data.get("nomor_kamar"), data.get("tipe"), harga)
    if kamar.nomor_kamar in kamar_db:
        raise ValueError(f"Kamar {kamar.nomor_kamar} sudah terdaftar.")
    kamar_db[kamar.nomor_kamar] = kamar
    return jsonify(_kamar_json(kamar)), 201

@app.get("/api/penghuni")
def daftar_penghuni():
    return jsonify([_penghuni_json(p) for p in penghuni_db.values()])

@app.post("/api/penghuni")
def tambah_penghuni():
    data = request.get_json(silent=True) or {}
    id_baru = f"P{len(penghuni_db) + 1:03d}"
    penghuni = Penghuni(id_baru, data.get("nama"), data.get("no_telpon"))
    penghuni_db[penghuni.id_penghuni] = penghuni
    return jsonify(_penghuni_json(penghuni)), 201

@app.post("/api/sewa")
def sewa_kamar():
    data = request.get_json(silent=True) or {}
    penghuni = penghuni_db.get(str(data.get("id_penghuni", "")).upper())
    kamar = kamar_db.get(str(data.get("nomor_kamar", "")).upper())
    if penghuni is None:
        raise ValueError("Penghuni belum terdaftar.")
    if kamar is None:
        raise ValueError("Kamar tidak ditemukan.")
    transaksi = penghuni.sewa_kamar(kamar, data.get("tanggal_masuk"))
    riwayat.append(transaksi)
    return jsonify(_sewa_json(transaksi)), 201

@app.post("/api/sewa/akhiri")
def akhiri_sewa():
    data = request.get_json(silent=True) or {}
    penghuni = penghuni_db.get(str(data.get("id_penghuni", "")).upper())
    if penghuni is None:
        raise ValueError("Penghuni belum terdaftar.")
    transaksi = penghuni.keluar_kamar(data.get("tanggal_keluar"))
    return jsonify(_sewa_json(transaksi))

@app.get("/api/laporan")
def laporan():
    return jsonify([_sewa_json(s) for s in reversed(riwayat)])

if __name__ == "__main__":
    app.run(debug=True)
