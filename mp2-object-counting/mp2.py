import cv2
import numpy as np
import matplotlib.pyplot as plt

img_bgr = cv2.imread('input/parking_ori.jpg')
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blurred, 50, 150)

kernel = np.ones((5, 5), np.uint8) # matrix 5x5

# menebalkan area tepi (2 iterasi supaya lebih jelas)
dilated =cv2.dilate(edges, kernel, iterations=2)
# menutup lubang di dalam objek
closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

plt.figure(figsize=(12, 8))
plt.subplot(2, 3, 1)
plt.imshow(img_rgb)
plt.title('Original Image')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(blurred, cmap='gray')
plt.title('Blurred Image')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(edges, cmap='gray')
plt.title('Edge Image')
plt.axis('off')


plt.subplot(2, 3, 4)
plt.imshow(dilated, cmap='gray')
plt.title('Dilated Image')
plt.axis('off')

plt.subplot(2, 3, 5)
plt.imshow(closed, cmap='gray')
plt.title('Closed Image')
plt.axis('off')


plt.show()