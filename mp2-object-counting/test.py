import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread('input/parking_ori.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 1. BLUR
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blurred, 40, 120)

# --- THE REAL PIPELINE ---

# Langkah 1: Dilasi Cukup Kuat
# Untuk menyambung garis-garis Canny yang putus
kernel_dilate = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(edges, kernel_dilate, iterations=2)

# --- THE MAGIC TRICK: CONTOUR FILLING ---
# Kita cari kerangka luarnya saja
contours_edges, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Buat canvas hitam kosong
solid_mask = np.zeros_like(gray) 

for cnt in contours_edges:
    area = cv2.contourArea(cnt)
    # Buang noise titik kecil dan mega-blob raksasa
    if 500 < area < 50000:
        # thickness=-1 (cv2.FILLED) adalah perintah untuk MEWARNAI/MENGISI bagian dalam kontur
        cv2.drawContours(solid_mask, [cnt], -1, 255, -1)

# Langkah 2: Closing Raksasa
# Menutup celah di antara kap mesin, atap, dan bagasi
# kernel_close = np.ones((25, 25), np.uint8)
# closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel_close)

# Langkah 3: Opening untuk membersihkan garis
kernel_open = np.ones((9, 9), np.uint8)
final_mask = cv2.morphologyEx(solid_mask, cv2.MORPH_OPEN, kernel_open)


# --- CONTOURS & FILL HOLES ---
# KUNCI BARU: cv2.RETR_TREE (Ambil semua kontur, lalu kita isi)
contours, hierarchy = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rectangles = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    
    # Filter Area (Jaring kita bikin sangat fleksibel)
    if 2500 < area < 25000:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        
        # Filter Bentuk
        if 0.3 < aspect_ratio < 3.0:
            # GAMBAR KOTAK (Hanya jika lolos)
            rectangles.append([x, y, w, h])
            rectangles.append([x, y, w, h])

grouped_rects, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

result_img = img_rgb.copy()
car_count = 0

for (x, y, w, h) in grouped_rects:
    cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 4)
    car_count += 1

# --- VISUALISASI ---
plt.figure(figsize=(15, 10))

# plt.subplot(2, 2, 1)
# plt.imshow(edges, cmap='gray')
# plt.title('1. Canny Edges')
# plt.axis('off')

plt.subplot(2, 2, 1)
plt.imshow(dilated, cmap='gray')
plt.title('2. Dilated (Sambung Putus)')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(solid_mask, cmap='gray')
plt.title('Solid Mask')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(final_mask, cmap='gray')
plt.title('3. Final Mask (Solid)')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(result_img)
plt.title(f'4. Counted Cars: {car_count}')
plt.axis('off')

plt.tight_layout()
plt.show()