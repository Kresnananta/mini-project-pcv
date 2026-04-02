import cv2
import numpy as np
import matplotlib.pyplot as plt

img_noisy = cv2.imread('../img/test_image_lena_noisy.png', cv2.IMREAD_GRAYSCALE)

if img_noisy is None:
    print('Image not found! please check your file')

def plot_histogram_manual(image, title):
    hist = np.zeros(256, dtype=int)

    tinggi, lebar, = image.shape

    for i in range(tinggi):
        for j in range(lebar):
            nilai_piksel = image[i, j]
            hist[nilai_piksel] += 1

    plt.figure(figsize=(12, 5))

    # gambar
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title('Citra')
    plt.axis('off')

    # histogram
    plt.subplot(1, 2, 2)
    plt.bar(range(256), hist, color='black', width=1)
    plt.title(title)
    plt.xlabel('Intensitas pixel (0-255)')
    plt.ylabel('Frekuensi')

    plt.show()

if img_noisy is not None:
    plot_histogram_manual(img_noisy, 'Histogram rusak')