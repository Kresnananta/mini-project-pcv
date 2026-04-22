import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. BACA GAMBAR
img_bgr = cv2.imread('input/parking_ori.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# --- TAHAP 1: PREPROCESSING & THRESHOLDING ---
# Blur sedang untuk membuang noise pasir
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# OTSU THRESHOLDING (PENGGANTI CANNY)
# Memisahkan area terang (mobil/garis) dan gelap (aspal) secara otomatis
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


# --- TAHAP 2: MORPHOLOGICAL CLEANING ---
# Masalah baru: Garis parkir ikut jadi putih.
# Solusi: Kita "hapus" garis putih yang tipis menggunakan Opening (Erosi lalu Dilasi)
# Kita pakai kernel bentuk "kotak" yang ukurannya disesuaikan untuk menghapus garis tapi mempertahankan mobil
kernel_open = np.ones((7, 7), np.uint8)
opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)

# Setelah garis parkir mulai hilang, kita padatkan lagi sisa mobilnya (Dilasi)
kernel_dilate = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(opened, kernel_dilate, iterations=1)


# --- TAHAP 3: CONTOURS & FILTERING ---
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result_img = img_rgb.copy()
car_count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)
    
    # FILTER AREA
    # Karena mobil sekarang berupa blok padat yang besar, batasnya bisa kita set lebar
    if 2500 < area < 15000: 
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        
        # FILTER BENTUK (Buang sisa garis parkir yang memanjang)
        if 0.4 < aspect_ratio < 2.5:
            cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 4)
            car_count += 1

# --- VISUALISASI ---
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
plt.imshow(thresh, cmap='gray')
plt.title('1. Otsu Threshold (Banyak Noise Garis)')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(opened, cmap='gray')
plt.title('2. Morph Opening (Garis Dihapus)')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(dilated, cmap='gray')
plt.title('3. Morph Dilation (Mobil Dipadatkan)')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(result_img)
plt.title(f'4. Hasil Akhir ({car_count} Mobil)')
plt.axis('off')

plt.tight_layout()
plt.show()