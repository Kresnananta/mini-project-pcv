import cv2
import numpy as np
import matplotlib.pyplot as plt

img_noisy = cv2.imread('input/test_image_lena_noisy.png', cv2.IMREAD_GRAYSCALE)



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



if __name__ == '__main__':
    # histogram image with noise 
    hist_noisy = plot_histogram(img_noisy)

    img_denoised, hist_denoised = apply_median_filter(img_noisy, kernel_size=3)

    img_equalized, hist_equalized = apply_histogram_eq(img_denoised, hist_denoised)

    plt.figure(figsize=(12, 7))

    # gambar noisy
    plt.subplot(3, 2, 1)
    plt.imshow(img_noisy, cmap='gray', vmin=0, vmax=255)
    plt.title('Image noisy')
    plt.axis('off')

    # histogram noisy
    plt.subplot(3, 2, 2)
    plt.bar(range(256), hist_noisy, color='black', width=1)
    plt.title('Histogram noisy')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    # gambar denoise
    plt.subplot(3, 2, 3)
    plt.imshow(img_denoised, cmap='gray', vmin=0, vmax=255)
    plt.title("Median Filter (denoised)")
    plt.axis('off')

    # histogram denoise
    plt.subplot(3, 2, 4)
    plt.bar(range(256), hist_denoised, color='black', width=1)
    plt.title('Histogram denoised (Median Filter)')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    # gambar equalized
    plt.subplot(3, 2, 5)
    plt.imshow(img_equalized, cmap='gray', vmin=0, vmax=255)
    plt.title("Image Equalized")
    plt.axis('off')

    # histogram equalize
    plt.subplot(3, 2, 6)
    plt.bar(range(256), hist_equalized, color='black', width=1)
    plt.title('Histogram Equalized')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    plt.tight_layout()
    plt.show()