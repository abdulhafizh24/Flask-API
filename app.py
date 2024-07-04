from flask import Flask, request, jsonify
import requests
import uuid
import datetime

app = Flask(__name__)

@app.route('/simulasi_biaya_impor', methods=['POST'])
def simulasi_biaya_impor():
    kode_barang = request.json['kode_barang']
    nilai_komoditas = request.json['nilai_komoditas']

    # Ambil uraian barang dari API
    url_barang = f"https://insw-dev.ilcs.co.id/my/n/barang?hs_code={kode_barang}"
    response_barang = requests.get(url_barang)
    if response_barang.status_code == 200:
        uraian_barang = response_barang.json()["uraian"]
    else:
        return jsonify({'error': 'Gagal mengambil data uraian barang'}), 400

    # Ambil tarif biaya impor dari API
    url_tarif = f"https://insw-dev.ilcs.co.id/my/n/tarif?hs_code={kode_barang}"
    response_tarif = requests.get(url_tarif)
    if response_tarif.status_code == 200:
        tarif_bm = response_tarif.json()["bm"]
    else:
        return jsonify({'error': 'Gagal mengambil data tarif biaya impor'}), 400

    # Hitung nilai BM
    nilai_bm = nilai_komoditas * tarif_bm / 100

    # Buat data simulasi
    data_simulasi = {
        "id_simulasi": str(uuid.uuid4()),
        "kode_barang": kode_barang,
        "uraian_barang": uraian_barang,
        "bm": tarif_bm,
        "nilai_komoditas": nilai_komoditas,
        "nilai_bm": nilai_bm,
        "waktu_insert": datetime.datetime.now().isoformat()
    }

    return jsonify(data_simulasi), 200

if __name__ == '__main__':
    app.run(debug=True)
