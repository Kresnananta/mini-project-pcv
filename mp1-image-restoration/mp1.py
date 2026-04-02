import cv2
import numpy as np
import matplotlib.pyplot as plt

img_noisy = cv2.imread('../img/test_image_lena_noisy.png', cv2.IMREAD_GRAYSCALE)



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



if __name__ == '__main__':
    # histogram image with noise 
    hist_noisy = plot_histogram(img_noisy)

    img_denoised, hist_denoised = apply_median_filter(img_noisy, kernel_size=3)

    plt.figure(figsize=(12, 7))

    # gambar noisy
    plt.subplot(2, 2, 1)
    plt.imshow(img_noisy, cmap='gray', vmin=0, vmax=255)
    plt.title('Image noisy')
    plt.axis('off')

    # histogram noisy
    plt.subplot(2, 2, 2)
    plt.bar(range(256), hist_noisy, color='black', width=1)
    plt.title('Histogram noisy')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    # gambar denoise
    plt.subplot(2, 2, 3)
    plt.imshow(img_denoised, cmap='gray', vmin=0, vmax=255)
    plt.title("Sesudah: Median Filter")
    plt.axis('off')

    # histogram denoise
    plt.subplot(2, 2, 4)
    plt.bar(range(256), hist_denoised, color='black', width=1)
    plt.title('Histogram denoised')
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    plt.tight_layout()
    plt.show()