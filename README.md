# Project Kalkulator Metode Secant
Beranggota:
- Muhammaad Fariz Alfisaputra (2408107010106)
- Roseline Balqist (2408107010079)
- Ahmad Zikri Pasya (2408107010103)
- T. Farid Haqi (2408107010091)
- M. Athallah Assyarif (2408107010088)

##Kalkulator Metode Secant Berbasis Web (Dokumentasi Lengkap)
Ini adalah aplikasi web yang dibangun dengan Python dan Flask untuk menemukan akar dari suatu fungsi menggunakan Metode Secant. Aplikasi ini menyediakan antarmuka interaktif di mana pengguna dapat memasukkan fungsi, tebakan awal, dan toleransi error untuk melihat hasil perhitungan, tabel iterasi langkah demi langkah, serta visualisasi grafik dari fungsi dan akarnya.

Penjelasan Rinci Kode Program
Proyek ini terdiri dari tiga file utama yang saling berinteraksi. Berikut adalah pembedahan lengkap dari setiap file.

1. app.py (Mesin Utama Aplikasi)
File ini adalah otak dari keseluruhan aplikasi. Ia menangani logika, perhitungan, dan berfungsi sebagai server web menggunakan framework Flask.

A. Impor Library dan Inisialisasi
    import matplotlib
    matplotlib.use('Agg')
    from flask import Flask, render_template, request
    import numpy as np
    import matplotlib.pyplot as plt
    import io
    import base64

    app = Flask(__name__)

    PRESET_FUNCTIONS = { ... }

    matplotlib.use('Agg'): Perintah ini sangat penting. Ia memberitahu Matplotlib untuk menggunakan backend "Agg", yang dirancang untuk membuat gambar tanpa perlu menampilkannya di layar (GUI). Ini wajib untuk aplikasi web di mana gambar dibuat di server.

    Flask: Kelas utama dari framework Flask untuk membuat aplikasi web.

    render_template: Fungsi untuk memuat file HTML dan memasukkan data dari Python ke dalamnya.

    request: Objek untuk mengakses data yang dikirim oleh pengguna (misalnya, dari form).

    numpy as np: Pustaka fundamental untuk komputasi numerik. Digunakan untuk fungsi matematika (sin, cos, exp) dan membuat larik angka (linspace) untuk grafik.

    matplotlib.pyplot as plt: Pustaka utama untuk membuat visualisasi data (grafik).

    io & base64: Digunakan untuk mengubah gambar grafik dari objek biner di memori menjadi teks (string Base64) agar bisa disematkan di HTML.

    app = Flask(__name__): Membuat instance dari aplikasi Flask.

    PRESET_FUNCTIONS: Sebuah dictionary Python yang menyimpan daftar fungsi siap pakai untuk ditampilkan di dropdown pada halaman web.

B. Fungsi safe_eval(expr, x_val)
    `def safe_eval(expr, x_val):
        allowed_names = { ... }
        code = compile(expr, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(...)
        return eval(code, {"__builtins__": {}}, allowed_names)`

    Tujuan: Mengevaluasi string fungsi matematika (mis., "x**2 - 4") dengan aman.

    Keamanan: Fungsi eval() bawaan Python bisa berbahaya jika pengguna memasukkan kode jahat. Fungsi ini membatasinya dengan hanya mengizinkan variabel (x) dan fungsi matematika yang telah ditentukan di dalam allowed_names. Jika pengguna mencoba menggunakan fungsi lain, aplikasi akan memunculkan error.

C. Fungsi secant_method(...)
    def secant_method(func_str, x0, x1, tol, max_iter=100):
        # ... (logika iterasi)

    Implementasi Algoritma: Ini adalah inti dari metode numerik Secant.

    Proses:

    Memulai loop iterasi.

    Di setiap iterasi, ia menghitung nilai x_next (aproksimasi akar berikutnya) menggunakan rumus Secant:
    x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

    Menghitung error absolut antara tebakan baru dan tebakan sebelumnya.

    Menyimpan semua data dari iterasi tersebut (n, x₀, x₁, f(x₀), f(x₁), dll.) ke dalam list iterations_data.

    Memeriksa apakah error sudah lebih kecil dari toleransi (tol). Jika ya, iterasi berhenti dan mengembalikan akar yang ditemukan.

    Jika belum, ia memperbarui nilai x0 dan x1 untuk persiapan iterasi berikutnya.

    Output: Mengembalikan tiga nilai: (hasil, pesan, data_iterasi).

D. Fungsi create_plot(...)
    def create_plot(func_str, x0, x1, root):
        # ... (logika plotting)

    Visualisasi Grafik: Fungsi ini bertanggung jawab untuk membuat gambar grafik.

    Proses:

    Menentukan rentang sumbu-x yang pas menggunakan np.linspace() agar fungsi dan akarnya terlihat jelas.

    Menggunakan plt.plot() dari Matplotlib untuk menggambar kurva fungsi.

    Menambahkan elemen visual seperti garis sumbu (axhline, axvline), judul, label, dan legenda.

    Menandai lokasi akar yang ditemukan dengan titik merah ('ro').

    Kunci: Grafik tidak disimpan sebagai file. Ia disimpan ke buffer di memori menggunakan io.BytesIO().

    base64.b64encode() kemudian mengubah data biner dari gambar di memori menjadi string teks. String inilah yang dikirim ke HTML.

E. Fungsi index() (Pengontrol Utama)
    @app.route("/", methods=["GET", "POST"])
    def index():
        # ... (logika penanganan request)

    Penanganan Rute: @app.route("/") memberitahu Flask bahwa fungsi ini akan menangani semua permintaan yang masuk ke halaman utama.

    Permintaan GET: Jika pengguna baru membuka halaman, metode request.method adalah GET. Fungsi ini hanya akan merender index.html dengan nilai-nilai default.

    Permintaan POST: Jika pengguna menekan tombol "Hitung Akar", form akan mengirim data dengan metode POST.

    request.form.get(...) digunakan untuk mengambil data dari setiap input form.

    Kode di dalam blok try...except mengubah input teks menjadi angka (float) dan menangani jika terjadi error (misalnya, input bukan angka).

    Memanggil secant_method() untuk melakukan perhitungan.

    Jika berhasil, memanggil create_plot() untuk membuat grafik.

    context.update({...}) memperbarui dictionary dengan hasil-hasil baru.

    Terakhir, render_template("index.html", **context) mengirim semua data di dalam context ke file HTML untuk ditampilkan.

2. templates/index.html (Struktur dan Tampilan Web)
File ini adalah kerangka dari halaman web. Ia bertanggung jawab untuk menampilkan antarmuka dan data yang dikirim oleh app.py.

    A. Struktur dan Form
    <form method="post">
        <select name="function_preset"> ... </select>
        <input type="number" name="x0" ...>
        ...
    </form>

    Menggunakan HTML5 standar dengan Bootstrap 5 untuk tata letak responsif (menggunakan kelas seperti .container, .row, .col-lg-5).

    Terdapat sebuah <form> dengan method="post" yang akan mengirimkan semua data input ke app.py saat tombol submit ditekan.

    B. Logika Templating (Jinja2)
    Jinja2 adalah template engine yang memungkinkan kita menyisipkan logika Python langsung di dalam HTML.

    {{ variabel }}: Digunakan untuk menampilkan nilai dari sebuah variabel yang dikirim dari Flask. Contoh: {{ result }} akan menampilkan nilai akar yang ditemukan.

    {% for ... %}: Digunakan untuk melakukan perulangan. Contohnya, untuk membuat opsi dropdown:

    {% for display, value in preset_functions.items() %}
        <option value="{{ value }}">{{ display }}</option>
    {% endfor %}

    Ini akan mengulang semua item di PRESET_FUNCTIONS dan membuat satu <option> untuk setiap fungsi.

    {% if ... %}: Digunakan untuk logika kondisional. Contohnya, tabel iterasi dan grafik hanya akan ditampilkan jika datanya ada:

    {% if iterations_data %}
        <!-- Tampilkan tabel di sini -->
    {% endif %}

    {% if plot_url %}
        <!-- Tampilkan grafik di sini -->
    {% endif %}

    Menampilkan Grafik: Baris ini sangat penting:

    <img src="data:image/png;base64,{{ plot_url }}">

    Atribut src memberitahu browser untuk tidak mencari file gambar, melainkan merender gambar langsung dari data teks Base64 yang ada di dalam variabel plot_url.

3. static/style.css (Desain Visual)
    File ini memberikan "pakaian" untuk kerangka HTML, menentukan warna, font, dan nuansa visual aplikasi.

    @import url(...): Mengimpor font kustom ('Poppins') dari Google Fonts untuk tipografi yang lebih modern.

    body: Mengatur gaya dasar untuk seluruh halaman, termasuk warna latar belakang gradien (linear-gradient) dan warna teks utama.

    .card: Mendefinisikan tampilan panel-panel utama, memberikan warna latar, border, dan bayangan (box-shadow) yang lembut untuk menciptakan efek visual yang bersih.

    Kustomisasi Elemen Form: Mengubah tampilan default dari input, select, dan tombol agar serasi dengan tema warna "Crème Brûlée". Efek :focus memberikan umpan balik visual saat pengguna berinteraksi dengan form.

    Kustomisasi Tabel: Mengubah warna header (.table-dark), baris ganjil (.table-striped), dan efek saat kursor diarahkan ke baris (.table-hover) agar menyatu dengan palet warna tema.

Cara Menjalankan Aplikasi
Pastikan Python terinstal.

Instal library yang dibutuhkan:

pip install Flask numpy matplotlib

Jalankan server Flask dari terminal:

python app.py
