# Project Kalkulator Metode Secant

## Anggota
- Muhammaad Fariz Alfisaputra (2408107010106)
- Roseline Balqist (2408107010079)
- Ahmad Zikri Pasya (2408107010103)
- T. Farid Haqi (2408107010091)
- M. Athallah Assyarif (2408107010088)
- Sayed Zaki Aqram (2408107010087)

---

## Kalkulator Metode Secant Berbasis Web

Aplikasi web ini dibangun dengan **Python** dan **Flask** untuk menemukan akar suatu fungsi menggunakan Metode Secant. Pengguna dapat memasukkan fungsi, nilai awal, dan toleransi, lalu melihat proses iterasi serta grafik interaktif.

---

### Penjelasan Rinci Kode Program

Proyek terdiri dari tiga file utama:

#### 1. `app.py` (Mesin Utama Aplikasi)

File ini sebagai otak aplikasi, menangani logika perhitungan dan berfungsi sebagai server web menggunakan Flask.

**A. Impor Library dan Inisialisasi**
```python
import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
PRESET_FUNCTIONS = { ... }
```
- `matplotlib.use('Agg')`: Agar Matplotlib bisa membuat gambar tanpa tampilan GUI.
- `Flask`, `render_template`, `request`: Untuk membangun aplikasi web dan mengelola data dari form.
- `numpy`: Komputasi numerik (fungsi matematika dan array).
- `matplotlib.pyplot`: Visualisasi grafik.
- `io`, `base64`: Konversi gambar ke teks agar bisa ditampilkan di HTML.
- `PRESET_FUNCTIONS`: Daftar fungsi siap pakai untuk dropdown web.

**B. Fungsi `safe_eval(expr, x_val)`**

Mengevaluasi string fungsi matematika secara aman menggunakan whitelist nama variabel dan fungsi matematika yang diperbolehkan. Mencegah eksekusi kode berbahaya.

**C. Fungsi `secant_method(...)`**

Implementasi algoritma Secant:
- Melakukan iterasi mencari akar.
- Menyimpan data tiap iterasi.
- Berhenti jika error sudah < toleransi.
- Mengembalikan hasil akar, pesan, dan data iterasi.

**D. Fungsi `create_plot(...)`**

Visualisasi grafik fungsi:
- Membuat rentang x yang sesuai.
- Plot fungsi, garis sumbu, dan titik akar.
- Menyimpan grafik ke buffer, lalu mengubahnya ke string Base64 agar bisa ditampilkan di HTML.

**E. Fungsi `index()` (Pengontrol Utama)**

Menangani route utama:
- GET: Render halaman awal.
- POST: Proses input form, hitung akar, buat grafik, dan tampilkan hasil.

---

#### 2. `templates/index.html` (Struktur dan Tampilan Web)

File ini membentuk tampilan antarmuka aplikasi dengan HTML dan Bootstrap 5.

- Form input fungsi, nilai awal, dan toleransi.
- Menggunakan Jinja2 untuk logika templating:
  - `{{ variabel }}`: Menampilkan data.
  - `{% for ... %}`: Perulangan, misal dropdown fungsi preset.
  - `{% if ... %}`: Menampilkan tabel iterasi dan grafik jika tersedia.
  - `<img src="data:image/png;base64,{{ plot_url }}">`: Grafik langsung dari data Base64.

---

#### 3. `static/style.css` (Desain Visual)

Mengatur tampilan aplikasi:
- Mengimpor font 'Poppins' dari Google Fonts.
- Background gradien, warna teks, dan card panel.
- Custom input, tombol, dan tabel agar serasi dengan tema warna.
- Efek hover dan fokus pada elemen interaktif.

---

## Cara Menjalankan Aplikasi

1. Pastikan **Python** telah terinstal.
2. Instal library yang dibutuhkan:
    ```
    pip install Flask numpy matplotlib
    ```
3. Jalankan server Flask dari terminal:
    ```
    python app.py
    ```

---

Selamat mencoba!
