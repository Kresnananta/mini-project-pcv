# Mini Project 1 - Image Restoration
- **Nama**: Anak Agung Ngurah Agung Kresna Ananta
- **NRP**: 5024241085

## Penjelasan Pipeline Restorasi
Pipeline restorasi ini diimplementasikan sepenuhnya menggunakan manipulasi *array* NumPy secara manual, tanpa menggunakan fungsi *processing* bawaan dari library OpenCV. Berikut adalah urutan teknik yang diterapkan:

1. **Denoising dengan Median Filter (Kernel 3x3):**
   - **Alasan Pemilihan:** Citra input mengalami kerusakan berupa *salt-and-pepper noise* yang parah (bintik hitam dan putih acak). [Median filter](https://en.wikipedia.org/wiki/Median_filter) dipilih karena sangat efektif mengeliminasi nilai piksel ekstrem (0 dan 255) dengan mengambil nilai median dari *neighborhood window*, sehingga *noise* tersebut hilang tanpa terlalu mengaburkan tepi objek (*edges*).
2. **Peningkatan Kontras dengan Histogram Equalization:**
   - **Alasan Pemilihan:** Setelah di-*denoise*, citra masih berstatus *low contrast* (distribusi warna sempit dan pudar). Teknik ini digunakan untuk meratakan distribusi intensitas piksel secara matematis menggunakan *[Cumulative Distribution Function](https://www.geeksforgeeks.org/engineering-mathematics/cumulative-distribution-function/)* (CDF). Hasilnya, rentang warna melebar penuh dari 0 hingga 255, membuat kontras citra kembali tajam.
   *(Catatan: Proses CDF dioptimalkan dengan mengambil data histogram langsung dari hasil perhitungan Median Filter sebelumnya agar menghemat komputasi).*

## Perbandingan Visual
| Citra Input (Noisy) | Citra Hasil Restorasi (Progress Saat Ini) |
| :---: | :---: |
| ![Noisy](input/test_image_lena_noisy.png) | ![Progress](path/ke/gambar/hasil/progress.png) |

## Analisis Singkat
- **Apa yang berhasil:** *Salt-and-pepper noise* berhasil dibersihkan dengan sangat memuaskan oleh Median Filter. Tingkat kecerahan dan kontras yang tadinya pudar juga sudah berhasil diperbaiki sepenuhnya melalui proses pemerataan histogram.
- **Apa yang bisa ditingkatkan:** Karena pemrosesan piksel dilakukan dengan perulangan (*nested loop*) manual, waktu eksekusi program (komputasi) berjalan lebih lambat dibandingkan jika menggunakan library C++ bawaan OpenCV. Secara visual, citra saat ini masih terlihat sedikit *blur* dan masih menyisakan sedikit *Gaussian noise*, yang akan diperbaiki di tahapan selanjutnya.

## Cara Menjalankan Program
1. Clone repository ini dan Masuk ke folder `mp1-image-restoration`:
    ```bash
    git clone https://github.com/Kresnananta/mini-project-pcv.git
    cd mp1-image-restoration
    ```
2. Pastikan Anda telah menginstal *library* prasyarat:
   ```bash
   pip install numpy matplotlib opencv-python
   ```
3. Pastikan file citra input `test_image_lena_noisy.png` berada pada direktori yang tepat (misalnya di folder `input/`).

4. Jalankan program:
    ```bash
    python mp1.py
    ```