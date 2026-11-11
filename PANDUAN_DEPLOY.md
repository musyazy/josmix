# Panduan GitHub + Streamlit Community Cloud (repo musyazy/konkret.id)

## A. Uji di komputer dulu (5 menit)

    python -m venv .venv
    .venv\Scripts\activate                 (macOS/Linux: source .venv/bin/activate)
    python -m pip install -r requirements.txt
    python -m utils.diagnostik             # semua baris wajib harus OK; PDF/QR/plotly boleh OPSIONAL
    streamlit run app.py

## B. Kirim perubahan ke GitHub (repo yang sudah ada)

1. Salin isi folder proyek ini ke folder repo `konkret.id` (timpa file; JANGAN hapus folder `.git`).
2. Pastikan folder tersembunyi ikut: `.streamlit/` (tema), `.gitignore`, `.python-version`.
3. Di terminal pada folder repo:

        git status
        git add -A                      # -A juga mencatat file yang dihapus/berganti nama
        git commit -m "Perbaikan ketahanan modul PDF dan requirements"
        git push origin main

   - Pertama kali: `git config --global user.name "Nama"` dan `git config --global user.email "email@gmail.com"`.
   - Saat diminta login, pakai GitHub Desktop / VS Code (Source Control) atau Personal Access Token (Settings > Developer settings > Tokens).
   - Mengunggah lewat web GitHub kurang cocok: folder `.streamlit` tersembunyi dan file lama yang sudah dihapus tidak ikut terhapus.
4. Cek di GitHub bahwa `app.py` ada di ROOT repo (bukan di dalam subfolder) dan `requirements.txt` terbaru terlihat.
5. JANGAN commit email, sandi, atau kunci: simpan di Secrets (bagian C). Folder `data/` sudah diabaikan oleh `.gitignore`.

## C. Streamlit Community Cloud

1. Buka https://share.streamlit.io, login dengan GitHub, izinkan akses ke repo.
2. **Create app** -> Repository `musyazy/konkret.id`, Branch `main`, Main file path `app.py`.
3. **Advanced settings**:
   - **Python version: pilih 3.12** (bawaan saat ini 3.14; rentang versi di requirements.txt tetap mendukung 3.14, tetapi 3.12 paling aman).
     Aplikasi yang sudah dibuat biasanya harus dihapus lalu dibuat ulang untuk mengganti versi Python.
   - **Secrets** (format TOML; kunci tingkat atas otomatis menjadi variabel lingkungan yang dibaca aplikasi):

         MIXDESIGN_AUTH_MODE = "email"
         MIXDESIGN_EMAIL_ADMIN = "adminanda@gmail.com"
         MIXDESIGN_ADMIN_PASSWORD = "sandi-panjang-acak"
         MIXDESIGN_EMAIL_IZIN = "rekan1@gmail.com,rekan2@gmail.com"

4. **Deploy**. Setiap `git push` ke `main` otomatis memperbarui aplikasi. Setelah mengubah requirements.txt atau Secrets:
   **Manage app (pojok kanan bawah) > menu titik tiga > Reboot app**.

## D. Membaca error (penting)

Layar aplikasi MENYEMBUNYIKAN isi error ("redacted"). Pesan lengkapnya ada di **Manage app > log**: cari baris terakhir
`ModuleNotFoundError: No module named '...'` atau `ImportError`; nama modul di situ adalah penyebabnya. Di dalam aplikasi, buka
tab **Laporan & CoA > Diagnostik modul cetak** (atau Panel Admin > Diagnostik lingkungan) untuk melihat versi Python dan modul yang gagal dimuat.

| Gejala | Penyebab | Solusi |
|---|---|---|
| Log: `Using Python 3.14` dan `Building numpy==1.26.4` / `pandas==2.2.3` | versi lama di-pin tanpa wheel Python 3.14 | pakai requirements.txt baru (rentang versi) dan/atau Python 3.12 |
| `ModuleNotFoundError` saat start | satu pustaka tidak terpasang/kompatibel | baca log; modul PDF/QR/grafik kini opsional sehingga aplikasi tetap hidup |
| Peringatan "PDF tidak dapat dibuat" | reportlab bermasalah di server | pakai unduhan Word/HTML; lihat Diagnostik; perbarui reportlab |
| Pengguna/permintaan akses hilang setelah reboot | disk Streamlit Cloud sementara | simpan whitelist tetap di Secrets (`MIXDESIGN_EMAIL_IZIN`); stok: pakai Supabase (lihat README) |
| Aplikasi "in the oven" lama | build dependensi dari sumber | pastikan Python 3.12 dan requirements baru |

## E. Perilaku di cloud yang perlu diketahui

- Data di folder `data/` (stok CSV, permintaan akses, persetujuan admin) hilang saat aplikasi di-reboot atau di-deploy ulang.
- Mode login `email` hanya pembatas akses (tidak memverifikasi pemilik email). Untuk keamanan nyata gunakan mode `google`
  (butuh `streamlit[auth]>=1.42` dan bagian [auth] di Secrets; lihat `.streamlit/secrets.toml.example`).
