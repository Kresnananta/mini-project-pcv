import cv2
import numpy as np
import matplotlib.pyplot as plt

PLT_COL = 2
PLT_ROW = 5
PLT_WIDTH = 12
PLT_HEIGHT = 12

img_noisy = cv2.imread('input/lena_noisy.png', cv2.IMREAD_GRAYSCALE)

if img_noisy is None:
    print('Image not found! please check your file')

def plot_histogram(image):
    hist = np.zeros(256, dtype=int) # array kosong noisy

    tinggi, lebar, = image.shape

    for i in range(tinggi):
        for j in range(lebar):
            nilai_piksel = image[i, j]
            hist[nilai_piksel] += 1 # masukin ke array
    
    return hist

def apply_median_filter(image, kernel_size=3):
    print('loading median filter ...')
    hist = np.zeros(256, dtype=int) # array median filter

    offset = kernel_size // 2
    tinggi, lebar = image.shape
    result = np.zeros((tinggi, lebar), dtype=np.uint8)

    padded_image = np.pad(image, offset, mode='constant', constant_values=0)

    for i in range(tinggi):
        for j in range(lebar):
            window = padded_image[i : i + kernel_size, j : j + kernel_size]

            window_flat = window.flatten()
            window_sorted = np.sort(window_flat)
            median_value = window_sorted[len(window_sorted) // 2]

            result[i, j] = median_value

            hist[result[i, j]] += 1
    
    return result, hist

def apply_mean_filter(image, hist):
    print('loading mean filter...')
    tinggi, lebar = image.shape
    result = np.zeros((tinggi, lebar), dtype=np.uint8)
    hist_temp = np.zeros(256, dtype=int)

    # Kernel rata-rata untuk mean filter
    kernel = np.ones((5, 5)) / 25.0

    offset = kernel.shape[0] // 2
    padded_image = np.pad(image, offset, mode='constant', constant_values=0)

    for i in range(tinggi):
        for j in range(lebar):
            window = padded_image[i : i + kernel.shape[0], j : j + kernel.shape[1]]

            value = np.sum(window * kernel)

            if value > 255:
                value = 255
            elif value < 0:
                value = 0

            result[i, j] = value
            hist_temp[result[i, j]] += 1

    return result, hist_temp

def apply_histogram_eq(image, hist):
    print('loading histogram equalization')
    tinggi, lebar = image.shape
    total_pixels = tinggi * lebar
    hist_temp = np.zeros(256, dtype=int)

    # Cumulative Distribution Func (CDF)
    cdf = np.zeros(256, dtype=int)
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + hist[i]

    # cari nilai CDF terkecil & bukan 0
    cdf_min = 0
    for val in cdf:
        if val > 0:
            cdf_min = val
            break
    
    # tabel mapping -> rumus normalisasi CDF
    mapping = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        if cdf[i] > 0:
            nilai_baru = round(((cdf[i] - cdf_min) / (total_pixels - cdf_min)) * 255)
            mapping[i] = nilai_baru

    result = np.zeros((tinggi, lebar), dtype=np.uint8)
    for i in range(tinggi):
        for j in range(lebar):
            nilai_lama = image[i, j]
            result[i, j] = mapping[nilai_lama]

            hist_temp[result[i, j]] += 1

    return result, hist_temp

def sharpening(image, hist):
    print('loading sharpening...')
    tinggi, lebar = image.shape
    result = np.zeros((tinggi, lebar), dtype=np.uint8)
    hist_temp = np.zeros(256, dtype=int)

    # Kernal laplacian untuk sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    offset = kernel.shape[0] // 2
    padded_image = np.pad(image, offset, mode='constant', constant_values=0)

    for i in range(tinggi):
        for j in range(lebar):
            window = padded_image[i : i + kernel.shape[0], j : j + kernel.shape[1]]

            value = np.sum(window * kernel)
            
            if value > 255:
                value = 255
            elif value < 0:
                value = 0

            result[i, j] = value
            hist_temp[result[i, j]] += 1

    return result, hist_temp



if __name__ == '__main__':
    img_noisy_color = cv2.imread('input/lena_noisy.png')

    if img_noisy_color is None:
        print('Image not found! please check your file')
        exit()
    
    img_noisy_rgb = cv2.cvtColor(img_noisy_color, cv2.COLOR_BGR2RGB)

    # Transformasi ke YCrCb
    img_ycrcb = cv2.cvtColor(img_noisy_color, cv2.COLOR_BGR2YCrCb)

    # split channel (Y = Luminance, Cr & Cb = Chrominance/Color)
    y, cr, cb = cv2.split(img_ycrcb)

    # histogram image with noise 
    print("Memproses Channel Y...")
    hist_noisy = plot_histogram(y)

    img_denoised, hist_denoised = apply_median_filter(y, kernel_size=3)
    img_mean_denoised, hist_mean_denoised = apply_mean_filter(img_denoised, hist_denoised)
    img_sharpened, hist_sharpened = sharpening(img_denoised, hist_denoised)
    img_equalized, hist_equalized = apply_histogram_eq(img_sharpened, hist_sharpened)

    # gabungkan channel Y yang udah diproses
    img_ycrcb_restored = cv2.merge((img_equalized, cr, cb))

    # ubah kembali ke RGB & BGR
    img_restored_rgb = cv2.cvtColor(img_ycrcb_restored, cv2.COLOR_YCrCb2RGB)
    img_restored_bgr = cv2.cvtColor(img_ycrcb_restored, cv2.COLOR_YCrCb2BGR)

    plt.figure(figsize=(PLT_WIDTH, PLT_HEIGHT))

    # gambar noisy (warna)
    plt.subplot(PLT_ROW, PLT_COL, 1)
    plt.imshow(img_noisy, cmap='gray', vmin=0, vmax=255)
    plt.title('Image noisy')
    plt.axis('off')

    # histogram noisy (channel Y)
    plt.subplot(PLT_ROW, PLT_COL, 2)
    plt.bar(range(256), hist_noisy, color='black', width=1)
    plt.title('Histogram noisy')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    # gamber mean denoise
    plt.subplot(PLT_ROW, PLT_COL, 3)
    plt.imshow(img_mean_denoised, cmap='gray', vmin=0, vmax=255)
    plt.title("Mean Filter (denoised)")
    plt.axis('off')

    # histogram mean denoise
    plt.subplot(PLT_ROW, PLT_COL, 4)
    plt.bar(range(256), hist_mean_denoised, color='black', width=1)
    plt.title('Histogram denoised (Mean Filter)')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    # gambar denoise
    plt.subplot(PLT_ROW, PLT_COL, 5)
    plt.imshow(img_denoised, cmap='gray', vmin=0, vmax=255)
    plt.title("Median Filter (denoised)")
    plt.axis('off')

    # histogram denoise
    plt.subplot(PLT_ROW, PLT_COL, 6)
    plt.bar(range(256), hist_denoised, color='black', width=1)
    plt.title('Histogram denoised (Median Filter)')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    # gambar sharpened
    plt.subplot(PLT_ROW, PLT_COL, 7)
    plt.imshow(img_sharpened, cmap='gray', vmin=0, vmax=255)
    plt.title('Sharpened')
    plt.axis('off')

    # histogram sharpened
    plt.subplot(PLT_ROW, PLT_COL, 8)
    plt.bar(range(256), hist_sharpened, color='black', width=1)
    plt.title('Histogram Sharpened')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')


    # GAMBAR HASIL AKHIR (BERWARNA)
    plt.subplot(PLT_ROW, PLT_COL, 9)
    plt.imshow(img_restored_rgb)
    plt.title("Final Image Equalized (COLOR)")
    plt.axis('off')

    # Histogram equalize (Y Channel)
    plt.subplot(PLT_ROW, PLT_COL, 10)
    plt.bar(range(256), hist_equalized, color='black', width=1)
    plt.title('Final Histogram (Y Channel)')


    plt.tight_layout()
    plt.show()

    cv2.imwrite('output/lena_restored_color.png', img_restored_bgr)
    print('Restored image saved in output/')