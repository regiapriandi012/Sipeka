from flask import Flask, render_template, redirect, url_for
from form import InputLaporan, InputKtp, CekKtp, CekLaporan
from flask_bootstrap import Bootstrap
from models import db, DataKtp, DataLaporan

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://doadmin:L8nQyZGwO5UiwcfG@sipekaid-do-user-8822551-0.b.db.ondigitalocean.com:25060/data_sipeka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()

#halaman untuk User
#----------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inputktp", methods=['GET', 'POST'])
def ktp():
    ktp_form = InputKtp(csrf_enabled=False)
    if ktp_form.validate_on_submit():
        nik = ktp_form.nik.data
        nama = ktp_form.nama.data
        ttl = ktp_form.ttl.data
        jk = ktp_form.jk.data
        alamat = ktp_form.alamat.data
        rt = ktp_form.rt.data
        rw = ktp_form.rw.data
        desa = ktp_form.desa.data
        kecamatan = "Banjarharjo"
        kabupaten = "Brebes"
        kewarganegaraan = "Indonesia"
        pekerjaan = ktp_form.pekerjaan.data
        status = ktp_form.status.data
        notelf = ktp_form.notelf.data
        status_validasi = "Data Belum Divalidasi"
        data_ktp = DataKtp(nik=nik, nama=nama, ttl=ttl, jk=jk, alamat=alamat, rt=rt, rw=rw,
                           desa=desa, kecamatan=kecamatan, kabupaten=kabupaten,
                           kewarganegaraan=kewarganegaraan, pekerjaan=pekerjaan,
                           status=status, notelf=notelf, status_validasi=status_validasi)
        try:
            db.session.add(data_ktp)
            db.session.commit()
        except:
            return redirect(url_for("input_ktp_gagal"))
        return redirect(url_for("input_ktp_success", nik=nik, nama=nama, _external=True))
    return render_template("inputKTP.html", ktp_form=ktp_form)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/inputlaporan", methods=['GET', 'POST'])
def laporan():
    laporan_form = InputLaporan(csrf_enabled=False)
    if laporan_form.validate_on_submit():
        nik = laporan_form.nik.data
        nama = laporan_form.nama.data
        rt = laporan_form.rt.data
        rw = laporan_form.rw.data
        desa = laporan_form.desa.data
        kecamatan = "Banjarharjo"
        jk = laporan_form.jk.data
        notelf = laporan_form.notelf.data
        kategory = laporan_form.kategory.data
        tanggal = laporan_form.tanggal.data
        isilaporan = laporan_form.isilaporan.data
        pernyataan = laporan_form.pernyataan.data
        status_validasi = "Data Belum DiValidasi"
        data_laporan = DataLaporan(nik=nik, nama=nama, rt=rt, rw=rw, desa=desa,
                                   kecamatan=kecamatan, jk=jk, notelf=notelf,
                                   kategory=kategory, tanggal=tanggal, isilaporan=isilaporan,
                                   pernyataan=pernyataan, status_validasi=status_validasi)
        try:
            db.session.add(data_laporan)
            db.session.commit()
        except:
            return redirect(url_for("input_laporan_gagal"))
        return redirect(url_for("input_lap_success", nik=nik, nama=nama, _external=True))
    return render_template("inputLaporan.html", laporan_form=laporan_form)

@app.route("/inputktp/reportsubmit/<nik>/<nama>", methods=['GET', 'POST'])
def input_ktp_success(nik, nama):
    return render_template("inputKTP_success.html", nama_form=nama, nik_form=nik)

@app.route("/inputlaporan/reportsubmit/<nik>/<nama>", methods=['GET', 'POST'])
def input_lap_success(nik, nama):
    return render_template("inputLaporan_success.html", nama_form=nama, nik_form=nik)

@app.route("/inputktp/gagal")
def input_ktp_gagal():
    return render_template("inputKTP_failed.html")

@app.route("/inputlaporan/gagal")
def input_laporan_gagal():
    return render_template("inputLaporan_failed.html")

@app.route("/inputktp/cekvalidasi", methods=['GET', 'POST'])
def cek_ktp():
    cek_ktp = CekKtp()
    if cek_ktp.validate_on_submit():
        try:
            nik = cek_ktp.nik.data
            nama = DataKtp.query.get(nik).nama
            status = DataKtp.query.get(nik).status_validasi
            return redirect(url_for("cek_status_ktp_sukses", nik=nik, nama=nama, status=status, _external=True))
        except:
            return redirect(url_for("cek_status_ktp_gagal"))
    return render_template("cek_KTP.html", cekKTP_form=cek_ktp)

@app.route("/inputlaporan/cekvalidasi", methods=['GET', 'POST'])
def cek_laporan():
    cek_laporan = CekLaporan()
    if cek_laporan.validate_on_submit():
        try:
            nik = cek_laporan.nik.data
            nama = DataLaporan.query.get(nik).nama
            status = DataLaporan.query.get(nik).status_validasi
            return redirect(url_for("cek_status_laporan_sukses", nik=nik, nama=nama, status=status, _external=True))
        except:
            return redirect(url_for("cek_status_laporan_gagal"))
    return render_template("cek_Laporan.html", cekLaporan_form=cek_laporan)

@app.route("/inputktp/cekvalidasi/<nik>/<nama>/<status>", methods=['GET', 'POST'])
def cek_status_ktp_sukses(nik, nama, status):
    return render_template("cekKTP_success.html", nama_form=nama, nik_form=nik, status_form=status)

@app.route("/inputlaporan/cekvalidasi/<nik>/<nama>/<status>", methods=['GET', 'POST'])
def cek_status_laporan_sukses(nik, nama, status):
    return render_template("cekLaporan_success.html", nama_form=nama, nik_form=nik, status_form=status)

@app.route("/inputktp/cekvalidasi/gagal")
def cek_status_ktp_gagal():
    return render_template("cekKTP_failed.html")

@app.route("/inputlaporan/cekvalidasi/gagal")
def cek_status_laporan_gagal():
    return render_template("cekLaporan_failed.html")

#--------------------------------------------
#halaman untuk Admin

@app.route("/admin/login")
def login_admin():
    return render_template("loginAdmin.html")

@app.route("/admin")
def admin():
    return render_template("indexAdmin.html")

@app.route("/admin/validasi/ktp")
def validasi_ktp():
    data_ktp = DataKtp.query.filter(DataKtp.status_validasi == 'Data Belum Divalidasi').all()
    return render_template("validasiKTP.html", data_ktp=data_ktp)

@app.route("/admin/validasi/laporan")
def validasi_laporan():
    data_laporan = DataLaporan.query.filter(DataLaporan.status_validasi == 'Data Belum Divalidasi').all()
    return render_template("validasiLaporan.html", data_laporan=data_laporan)

@app.route("/admin/validasi/ktp/<nik>")
def validasi_ktp_data(nik):
    data_ktp = DataKtp.query.get(nik)
    return render_template("validasiKTP_data.html", data_ktp=data_ktp)

@app.route("/admin/validasi/laporan/<nik>")
def validasi_laporan_data(nik):
    data_laporan = DataLaporan.query.get(nik)
    return render_template("validasiLaporan_data.html", data_laporan=data_laporan)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)